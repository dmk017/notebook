from io import BytesIO
import mimetypes
import openpyxl
from typing import Optional
from fastapi import (APIRouter, Depends,
                    UploadFile, Response, BackgroundTasks)
from returns.pipeline import is_successful

from src.auth.data.auth_repository import get_auth_user_by_id
from src.utils.io.zip import create_zip_buffer
from src.objects.objects_service_schema import CountObjectsResposnse
from src.utils.fp.get_or_else_w import get_or_else_w
from returns.pipeline import flow
from src.errors.errors import Errors
from src.models import models_service
from src.models.data import models_repository
from src.objects import objects_service
from src.objects.data import objects_repository
from src.objects.objects_router_api_schema import (
    AddObjectRequest,
    AddObjectResponse,
    SearchObject,
    ApproveDeclineShem
)

from src.objects.utils.objects_row_parser import row_to_property_parser
from src.types.pagination import ListResponse
from src.types.response import ReponseError, buffer_file_response
from src.auth.objects_auth import objects_auth

from src.objects.data.objects_schema import ObjectSchema


from src.keycloak.keycloak_integration import get_user_info
from src.keycloak.keycloak_models import User


router = APIRouter(
    prefix="/objects",
    tags=["objects"]
)


@router.get(
    path="/",
    response_model=ListResponse
)
async def get_all_objects(page: int = 1, limit: int = 10, user: User = Depends(get_user_info)):
    filters = []
    auth_data = objects_auth.auth_get_all_objects(user, filters)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    available_models_list = models_service.get_available_models_by_user_id(
        user_id=auth_data.unwrap().user_id,
        user_role=user.role
    )
    objects = objects_service.get_objects_by_filter(page=page, limit=limit, filters=filters, model_ids=[str(model.id) for model in available_models_list])
    return ListResponse(
        count=len(objects),
        page_number=page,
        is_next=len(objects) == limit,
        data=objects
    )


@router.get(
    path="/count",
    response_model=CountObjectsResposnse
)
async def get_count_objects(page: int = 1, limit: int = 10, user: User = Depends(get_user_info)):
    filters = []
    auth_data = objects_auth.auth_get_all_objects(user, filters)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    available_models_list = models_service.get_available_models_by_user_id(
        user_id=auth_data.unwrap().user_id,
        user_role=user.role
    )
    objects_count = objects_service.get_objects_count_by_filter(filters=filters, model_ids=[str(model.id) for model in available_models_list])
    return CountObjectsResposnse(
        total=objects_count
    )


@router.post(
    path="/",
    response_model=ObjectSchema
)
async def add_object(add_object_form: AddObjectRequest = Depends(AddObjectRequest), user: User = Depends(get_user_info)):
    auth_data = objects_auth.auth_add_object(user, add_object_form.payload.model_id)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(objects_service.add_object(
        owner_id=user.user_id,
        model_id=add_object_form.payload.model_id,
        properties=add_object_form.payload.properties
        ),
        get_or_else_w(on_failure= lambda error: error)
    )

    return result


@router.get(
    path="/{id}",
    response_model=Optional[ObjectSchema]
)
async def get_object(id: str, user: User = Depends(get_user_info)):
    object = objects_repository.get_object_by_id(id)
    if object is None:
        return None
    auth_data = objects_auth.auth_get_object(user, object)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return object


@router.post(
    path="/package/file",
    response_model=AddObjectResponse
)
async def upload_file(file: UploadFile, user: User = Depends(get_user_info)):
    errors: list[ReponseError] = []
    file_bytes = BytesIO(await file.read())
    file_bytes.seek(0)
    wb = openpyxl.load_workbook(file_bytes)
    worksheet = wb.active
    model_name = worksheet.title
    auth_data = objects_auth.auth_upload_file(user, model_name)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    model = models_repository.get_actual_model_by_name(model_name)
    if model is None:
        errors.append(
            ReponseError(
                code=Errors.MODEL_NOT_FOUND_4003.value,
                details=f'Моель с названием "{model_name}" не найдена'
            )
        )
        return _add_object_response(errors)

    model_id = str(model.id)
    rows = worksheet.rows
    property_names = list(map(lambda item: item.value, next(rows)))
    property_primitive_names = list(map(lambda item: item.value, next(rows)))
    next(rows)  # пропускаем подсказку
    property_primitive_names = list(
        zip(property_names, property_primitive_names)
    )
    objects_properties = []
    for row_num, row in enumerate(rows, 3):
        temp_dict = {}
        for ceil_num, ceil in enumerate(row, 0):
            temp_dict[
                "_".join(property_primitive_names[ceil_num])
            ] = str(ceil.value)
        data = row_to_property_parser(temp_dict)
        validate = objects_service.validate_object(
            owner_id=user.user_id,
            model_id=model_id,
            properties=data
        )
        if not is_successful(validate):
            errors += list(map(lambda e: ReponseError.parse_obj({
                **e.dict(),
                "details": f'Строка №{row_num + 1}: {e.details}'
            }), validate.failure()))
        else:
            objects_properties.append(validate.unwrap())

    if errors:
        return _add_object_response(errors, "")

    for proprties in objects_properties:
        new_object = objects_service.add_object(
            owner_id=user.user_id,
            model_id=model_id,
            properties=proprties
        )
        if not is_successful(new_object):
            print(new_object.failure())
    return _add_object_response(
        errors=[],
        success_message=f"Success added {len(objects_properties)} objects"
    )


def _add_object_response(errors, success_message=''):
    return AddObjectResponse(
        success=not len(errors),
        errors=errors,
        message=success_message if not len(errors) else ''
    )


@router.post(
    path="/search",
    response_model=ListResponse
)
async def objects_search(search_object: SearchObject, user: User = Depends(get_user_info)):
    page = search_object.page
    count = search_object.count
    text = search_object.text
    filters = search_object.filters
    auth_data = objects_auth.auth_search_objects(user, filters)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    available_models_list = models_service.get_available_models_by_user_id(
        user_id=auth_data.unwrap().user_id,
        user_role=user.role
    )
    objects = objects_service.get_objects_by_filter(
        page=page,
        limit=count,
        filters=filters,
        model_ids=[str(model.id) for model in available_models_list],
        text=text
    )

    return ListResponse(
        count=len(objects),
        page_number=page,
        is_next=len(objects) == count,
        data=objects
    )


@router.put(
    path="/decline",
    response_model=int
)
async def decline_objects(approve_decline_shem: ApproveDeclineShem, user: User = Depends(get_user_info)):
    auth_data = objects_auth.auth_decline_objects(user, approve_decline_shem)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    if approve_decline_shem.objectsId is not None:
        return objects_service.change_status_objects(
            'decline',
            approve_decline_shem.objectsId,
            user.user_id,
            reason=approve_decline_shem.reason
        )
    return objects_service.change_status_objects(
            'decline',
            objects_service.get_objects_ids_by_filters(approve_decline_shem.filters),
            user.user_id,
            reason=approve_decline_shem.reason
        )


@router.put(
    path="/approve",
    response_model=int
)
async def approve_objects(approve_decline_shem: ApproveDeclineShem, user: User = Depends(get_user_info)):
    auth_data = objects_auth.auth_approve_objects(user, approve_decline_shem)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    if approve_decline_shem.objectsId is not None:
        return objects_service.change_status_objects(
            'approve',
            approve_decline_shem.objectsId,
            user.user_id,
            reason=approve_decline_shem.reason
        )
    return objects_service.change_status_objects(
            'approve',
            objects_service.get_objects_ids_by_filters(approve_decline_shem.filters),
            user.user_id,
            reason=approve_decline_shem.reason
        )


@router.post(
    path='/unloading',
    response_class=Response
)
async def unloading_objects(search_object: SearchObject, background_tasks: BackgroundTasks, user: User = Depends(get_user_info)):
    auth_data = objects_auth.auth_unloading_objects(user, search_object.filters)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    available_models_list = models_service.get_available_models_by_user_id(
        user_id=auth_data.unwrap().user_id,
        user_role=user.role
    )
    objects = objects_service.get_objects_by_filter(
        page=search_object.page,
        limit=search_object.count,
        filters=search_object.filters,
        model_ids=[str(model.id) for model in available_models_list],
        text=search_object.text
    )

    temp_buffer_xlsx = []
    objects_by_model = objects_service.grouping_objects_by_attribute(attribute='model_id', objects=objects)

    for model_id, objects in objects_by_model.items():
        objects_by_owner = objects_service.grouping_objects_by_attribute(attribute='owner_id', objects=objects)
        for owner_id, objects in objects_by_owner.items():
            owner = get_auth_user_by_id(owner_id)
            temp_buffer_xlsx.append(objects_service.create_file_unloading(model_id=model_id, owner_name=owner.user_name, objects=objects))

    zip_name = f'{user.user_id}_result_search.zip'
    zip_buffer = create_zip_buffer(temp_buffer_xlsx)
    return buffer_file_response(
        buffer=zip_buffer,
        filename=zip_name,
        media_type=mimetypes.types_map['.zip']
    )
