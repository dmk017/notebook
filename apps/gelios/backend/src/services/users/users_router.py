from src.config import get_settings
from src.services.keycloak.keycloak_models import User
from fastapi import APIRouter, Depends, status, HTTPException
from src.services.keycloak.keycloak_integration import get_user_info
from src.utils.requests_handler import get_group_members, GroupMembers


router = APIRouter(prefix="/users", tags=["users"])
settings = get_settings()


@router.get(path="/list", status_code=status.HTTP_200_OK, response_model=GroupMembers)
async def get_users(
    user_info: tuple[User, str] = Depends(get_user_info),
):
    _, token = user_info
    try:
        return get_group_members(token=token)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
