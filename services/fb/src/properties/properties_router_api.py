from fastapi import APIRouter, Depends, Response
from returns.pipeline import flow, is_successful
from typing import Union, Optional



from src.properties import properties_service
from src.properties.data import properties_repository
from src.properties.properties_exceptions_http import \
    properties_fail_http_resolver
from src.properties.properties_router_api_schema import \
    AddPropertySchemaRequest, PropertyListFilters

from src.utils.fp.get_or_else_w import get_or_else_w


from src.keycloak.keycloak_integration import get_user_info
from src.keycloak.keycloak_models import User

from src.properties.data.properties_schema import  PropertySchema
from src.auth.properties_auth import properties_auth

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.post(
    path='/list',
    response_model=list[PropertySchema]
)
async def get_properties(filters: PropertyListFilters, page: int = 1, limit: int = 10,  user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_get_properties(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return properties_repository.get_actual_properties(filters, page=page, limit=limit)


@router.post(
    path="/",
    response_model=PropertySchema
)
async def add_property(add_property_form: AddPropertySchemaRequest = Depends(AddPropertySchemaRequest), user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_add_property(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        properties_service.add_property(
            name=add_property_form.payload.name,
            properties=add_property_form.payload.properties,
            user_id=user.user_id
        ),
        get_or_else_w(
            on_failure=properties_fail_http_resolver
        )
    )
    return result


@router.get(
    path='/{id}',
    response_model=Optional[PropertySchema]
)
async def get_property_by_id(id: str, user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_get_property_by_id(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return properties_service.get_property_by_id(id)

@router.get(
    path='/{id}/history',
    response_model=list[PropertySchema]
)
async def get_property_history(id: str, user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_get_property_by_id(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    return properties_service.get_property_history(id)
    

@router.put(
    path="/{id}",
    response_model=PropertySchema
)
async def update_property(id: str, add_property_form: AddPropertySchemaRequest = Depends(AddPropertySchemaRequest), user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_update_property(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        properties_service.update_property(
            name=add_property_form.payload.name,
            properties=add_property_form.payload.properties,
            user_id=user.user_id
        ),
        get_or_else_w(
            on_failure=properties_fail_http_resolver
        )
    )
    return result


@router.delete(
    path="/{id}",
    response_model=PropertySchema
)
async def delete_property(id: str, user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_delete_property(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        properties_service.recove_delete_property(
            id=id,
            deleted=True
        ),
        get_or_else_w(
            on_failure=properties_fail_http_resolver
        )
    )
    return result


@router.post(
    path="/{id}/recove",
    response_model=PropertySchema
)
async def recove_property(id: str, user: User = Depends(get_user_info)):
    auth_data = properties_auth.auth_recove_property(user)
    if not is_successful(auth_data):
        return Response(status_code=auth_data.failure().value.code, content=auth_data.failure().value.message)
    result = flow(
        properties_service.recove_delete_property(
            id=id,
            deleted=False
        ),
        get_or_else_w(
            on_failure=properties_fail_http_resolver
        )
    )
    return result

