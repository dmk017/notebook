from returns.result import Result, Success, Failure
from typing import Any, Optional

from src.auth.data.auth_repository import get_auth_user_by_id
from src.auth.data.auth_schema import AuthSchema, AuthErrors

from src.keycloak.keycloak_models import User, UserRole


def auth_get_properties(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)
    

def auth_add_property(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_get_property_by_id(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)


def auth_update_property(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_delete_property(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)

def auth_recove_property(user: User) -> Result[Any, AuthErrors]:
    current_user = get_auth_user_by_id(user_id=user.user_id, user_name=user.user_name)
    if current_user is None:
        return Failure(AuthErrors.INVALID_SERVER)
    if user.role.value == UserRole.ADMIN.value:
        return Success(current_user)
    return Failure(AuthErrors.ACCESS_DENIED)
