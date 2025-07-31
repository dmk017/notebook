from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import FileResponse
from returns.pipeline import flow, is_successful
from typing import Optional, Union
import mimetypes

from src.errors.errors import Errors

from src.types.response import buffer_file_response
from src.types.pagination import ListResponse
from src.models import models_service
from src.models.data import models_repository
from src.properties import properties_service
from src.models.models_exceptions_http import models_fail_http_resolver
from src.models.models_router_api_schema import AddModelRequest, ModelsListFilter, ResponseModel, ResponsePropertyPayload
from src.utils.fp.get_or_else_w import get_or_else_w

from src.keycloak.keycloak_integration import get_user_info
from src.keycloak.keycloak_models import User

from src.models.data.models_schema import  ModelSchema, ModelPropertyPayload
from src.auth.models_auth import models_auth


router = APIRouter(
    prefix="/models",
    tags=["models"]
)


@router.post(
    path="/list",
    response_model=ListResponse
)
async def get_models(filters: ModelsListFilter, page: int = 1, limit: int = 10, user: User = Depends(get_user_info)):
    auth_data = models_auth.auth_get_models(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    models = models_repository.get_models(filters=filters, page=page, limit=limit, available_models_id=auth_data.unwrap()['available_models_id'])
    return ListResponse(
        count=len(models),
        page_number=page,
        is_next=len(models) == limit,
        data=list(map(decode_model, models))
    )



@router.get(
    path="/{id}",
    response_model=Optional[ResponseModel]
)
async def get_model_by_id(id: str, user: User = Depends(get_user_info)):
    model = models_service.get_model_by_id(id)
    if model is None:
        return Response(status_code=400, content=Errors.MODEL_NOT_FOUND_4003.value.message)
    auth_data = models_auth.auth_get_model_by_id(user, model)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return decode_model(model)


@router.get(
    path='/{id}/history',
    response_model=list[ResponseModel]
)
async def get_model_history(id: str, user: User = Depends(get_user_info)):
    model = models_service.get_model_by_id(id)
    auth_data = models_auth.auth_get_model_by_id(user, model)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return list(map(decode_model, models_service.get_model_history(id)))


@router.post(
    path="/",
    response_model=ModelSchema
)
async def add_model(add_object_form: AddModelRequest = Depends(AddModelRequest), user: User = Depends(get_user_info)):
    auth_data = models_auth.auth_add_model(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        models_service.add_model(
            name=add_object_form.payload.name,
            properties=[ModelPropertyPayload.model_validate(elem.dict()) for elem in add_object_form.payload.properties],
            user_id=user.user_id
        ),
        get_or_else_w(
            on_failure=models_fail_http_resolver
        )
    )
    return result


@router.put(
    path="/{id}",
    response_model=ModelSchema
)
async def update_model(id: str, add_object_form: AddModelRequest = Depends(AddModelRequest), user: User = Depends(get_user_info)):
    auth_data = models_auth.auth_update_model(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        models_service.update_model(
            name=add_object_form.payload.name,
            properties=[ModelPropertyPayload.model_validate(elem.dict()) for elem in add_object_form.payload.properties],
            user_id=user.user_id
        ),
        get_or_else_w(
            on_failure=models_fail_http_resolver
        )
    )
    return result


@router.delete(
    path="/{id}",
    response_model=ModelSchema
)
async def delete_model(id:str, user: User = Depends(get_user_info)):
    auth_data = models_auth.auth_delete_model(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        models_service.recove_delete_model(
            id=id,
            deleted=True
        ),
        get_or_else_w(
            on_failure=models_fail_http_resolver
        )
    )
    return result


@router.post(
    path="/{id}/recove",
    response_model=ModelSchema
)
async def recove_model(id: str, user: User = Depends(get_user_info)):
    auth_data = models_auth.auth_recove_model(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        models_service.recove_delete_model(
            id=id,
            deleted=False
        ),
        get_or_else_w(
            on_failure=models_fail_http_resolver
        )
    )
    return result

@router.get(
    path='/{id}/example/file',
    response_class=FileResponse
)
async def get_example_file_modedl(id: str, user: User = Depends(get_user_info)):
    model_name = models_service.get_model_by_id(id).name
    auth_data = models_auth.auth_get_example_file_modedl(user, model_name)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    tempfile = models_service.create_model_template_file(id)
    return buffer_file_response(
        buffer=tempfile.buffer,
        filename=tempfile.name,
        media_type=mimetypes.types_map['.xls']
    )


def decode_model(model: ModelSchema) -> ResponseModel:
    def get_response_property(p: ModelPropertyPayload) -> ResponsePropertyPayload:
        result = properties_service.get_property_by_id(p.id)
        return ResponsePropertyPayload(
            payload=result,
            is_required=p.is_required
        )
    return ResponseModel(
        id=model.id,
        name=model.name,
        owner_id=model.owner_id,
        created_at=model.created_at,
        next_id=model.next_id,
        deleted=model.deleted,
        properties=list(map(get_response_property, model.properties))
    )
