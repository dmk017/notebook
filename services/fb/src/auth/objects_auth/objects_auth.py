from returns.result import Result, Success, Failure
from typing import Any, Optional

from src.auth.data.auth_repository import get_auth_user_by_id
from src.auth.data.auth_schema import AuthSchema, AuthErrors
from src.auth.objects_auth.utils.objects_auth_utils import parse_filters_auth
from src.objects.objects_router_api_schema import SearchFiltersList, SearchFilter

from src.keycloak.keycloak_models import User, UserRole
from src.objects.data.objects_schema import ObjectSchema
from src.models.models_service import get_model_by_id
from src.objects import objects_service
from src.objects.data import objects_repository
from src.models.models_service import get_available_models_by_user_id

from src.objects.objects_router_api_schema import ApproveDeclineShem

def auth_get_all_objects(user: User, filters: list[SearchFiltersList]) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value or user.role.value == UserRole.MODERATOR.value:
        return Success(current_user)
    add_filter_by_owner_id(filters, current_user.user_id)
    return Success(current_user)

def auth_add_object(user: User, model_id: str) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    model_name = get_model_by_id(model_id).name
    return Success(current_user) if model_name in current_user.access_model_names else Failure(AuthErrors.ACCESS_DENIED)

def auth_get_object(user: User, object: ObjectSchema) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.MODERATOR.value:
        model_name = get_model_by_id(str(object.model_id)).name
        return Success(current_user) if model_name in current_user.access_model_names else Failure(AuthErrors.ACCESS_DENIED)
    if (user.role.value == UserRole.ADMIN.value) or (object.owner_id == user.user_id):
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)
    
def auth_upload_file(user: User, model_name: str) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if (user.role.value == UserRole.ADMIN.value) or model_name in current_user.access_model_names:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_search_objects(user: User, filters: list[SearchFiltersList]) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value or user.role.value == UserRole.MODERATOR.value:
        return Success(current_user)
    
    list_owner_ids = parse_filters_auth(filters, 'owner_id')['owner_id']

    if len(list_owner_ids) == 0:
        add_filter_by_owner_id(filters, current_user.user_id)
    else:
        for owner_id in list_owner_ids:
            if owner_id != current_user.user_id:
                return Failure(AuthErrors.ACCESS_DENIED)
    return Success(current_user)

def auth_unloading_objects(user: User, filters: list[SearchFiltersList]) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value or user.role.value == UserRole.MODERATOR.value:
        return Success(current_user)
    
    list_owner_ids = parse_filters_auth(filters, 'owner_id')['owner_id']

    if len(list_owner_ids) == 0:
        add_filter_by_owner_id(filters, current_user.user_id)
    else:
        for owner_id in list_owner_ids:
            if owner_id != current_user.user_id:
                return Failure(AuthErrors.ACCESS_DENIED)
    return Success(current_user)

def auth_decline_objects(user: User, approve_decline_shem: ApproveDeclineShem) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    if user.role.value == UserRole.MODERATOR.value:
        obj_ids = approve_decline_shem.objectsId if approve_decline_shem.objectsId else objects_service.get_objects_ids_by_filters(approve_decline_shem.filters)
        for obj_id in obj_ids:
            if str(objects_repository.get_object_by_id(str(obj_id)).model_id) not in [str(model.id) for model in get_available_models_by_user_id(user.user_id, user.role)]:
                return Failure(AuthErrors.ACCESS_DENIED)
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_approve_objects(user: User, approve_decline_shem: ApproveDeclineShem) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    if user.role.value == UserRole.MODERATOR.value:
        obj_ids = approve_decline_shem.objectsId if approve_decline_shem.objectsId else objects_service.get_objects_ids_by_filters(approve_decline_shem.filters)
        for obj_id in obj_ids:
            if str(objects_repository.get_object_by_id(str(obj_id)).model_id) not in [str(model.id) for model in get_available_models_by_user_id(user.user_id, user.role)]:
                return Failure(AuthErrors.ACCESS_DENIED)
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)


def add_filter_by_owner_id(filters: list[SearchFiltersList], owner_id: str) -> bool:
    for filter in filters:
        if isinstance(filter, SearchFiltersList) and filter.group == 'AND':
            filter.conditions.append(SearchFilter(type='isolated',property='owner_id', operator='eq', value=str(owner_id)))
            return
    filters.append(SearchFiltersList(type='group', group='AND', conditions=[SearchFilter(type='isolated',property='owner_id', operator='eq', value=str(owner_id))]))
    return