from fastapi import APIRouter, Depends
from src.services.keycloak.keycloak_models import User
from src.services.keycloak.keycloak_integration import get_user_info


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(path="/me", response_model=User)
async def get_me(
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    return user
