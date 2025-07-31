from returns.result import Result, Success, Failure
from typing import Any, Optional

from src.auth.data.auth_repository import get_auth_user_by_id
from src.auth.data.auth_schema import AuthSchema, AuthErrors
from src.models.data.models_schema import  ModelSchema

from src.keycloak.keycloak_models import User, UserRole
from src.models.models_service import get_available_models_by_user_id

def auth_get_models(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    available_models_id = []
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success({'available_models_id' : available_models_id})
    available_models = get_available_models_by_user_id(user_id=user.user_id, user_role=user.role)
    available_models_id = [str(model.id) for model in available_models]
    if len(available_models_id) == 0:
        return Failure(AuthErrors.ACCESS_DENIED)
    return Success({'available_models_id' : available_models_id})
    
    
def auth_get_model_by_id(user: User, model: ModelSchema) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if (user.role.value == UserRole.ADMIN.value):
        return Success(current_user)
    if model.name in current_user.access_model_names:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_add_model(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_update_model(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_delete_model(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_recove_model(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_get_example_file_modedl(user: User, model_name: str) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    if model_name in current_user.access_model_names:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)
