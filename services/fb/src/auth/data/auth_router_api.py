from fastapi import APIRouter, Depends, Response
from typing import Optional

from pydantic import BaseModel
from src.auth.data.auth_schema import AuthSchema, ChangeAccessModelsSchema
from src.auth.data.auth_repository import get_auth_user_by_id, update_access_model_names 

from src.keycloak.keycloak_integration import get_user_info, get_user_token
from src.keycloak.keycloak_models import User, UserRole
from src.auth.data.auth_schema import AuthSchema
from src.models import models_service
from src.auth.data.auth_utils import check_exist_model
from src.errors.errors import Errors

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get(
    path="/me",
    response_model=User
)
async def get_me(user: User = Depends(get_user_info)):
    return user


class UserTokenResponse(BaseModel):
    token: str

@router.get(
    path="/token",
    response_model=UserTokenResponse
)
async def get_token(token: str = Depends(get_user_token)):
    return UserTokenResponse(token=token)

@router.get(
    path="/{user_id}",
    response_model=Optional[AuthSchema]
)
async def get_user(user_id: str, user: User = Depends(get_user_info)) -> Optional[AuthSchema]:
    if not (user.role.value == UserRole.ADMIN.value or user.role.value == UserRole.MODERATOR.value):
        return Response(status_code=403)
    return get_auth_user_by_id(user_id=user_id)


@router.put(
    path="/models",
    response_model=Optional[AuthSchema]
)
async def update_access_models(change_access_models_schema: ChangeAccessModelsSchema = Depends(ChangeAccessModelsSchema), user: User = Depends(get_user_info)) -> Optional[AuthSchema]:
    if not (user.role.value == UserRole.ADMIN.value):
        return Response(status_code=403)
    
    if not check_exist_model(change_access_models_schema.access_model_names):
        return Response(status_code=400, content=Errors.MODEL_NOT_FOUND_4003.value.message)

    return update_access_model_names(
        user_id=change_access_models_schema.user_id,
        owner_id=user.user_id,
        access_model_names=change_access_models_schema.access_model_names
    )
