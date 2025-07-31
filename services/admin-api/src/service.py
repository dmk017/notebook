from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.utils import flatten
from src.keycloak.keycloak_admin_integration import get_keycloak_admin
from src.schemas import GroupData, UserData
from src.keycloak.keycloak_admin_integration import get_keycloak_admin

from src.config import get_settings
from src.schemas import UserData

settings = get_settings()

router = APIRouter(
    prefix="",
    tags=[""]
)

@router.get(
    path='/users/{user_id}',
    response_model=Optional[UserData]
)
def get_user_by_id(user_id: str, admin = Depends(get_keycloak_admin)):
    try:
      return admin.get_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

@router.get(
    path='/users/{user_id}/groups',
    response_model=list[GroupData]
)
def get_user_groups(user_id: str, admin = Depends(get_keycloak_admin)):
    try:
        return admin.get_user_groups(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

@router.get(
    path='/groups/{group_id}',
    response_model=GroupData
)
def get_group_by_id(group_id: str, admin = Depends(get_keycloak_admin)):
    try:
      return admin.get_group(group_id=group_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )

@router.get(
    path='/groups/{group_id}/members',
    response_model=list[UserData]
)
def get_group_by_id(group_id: str, admin = Depends(get_keycloak_admin)):
    try:
        return admin.get_group_members(group_id=group_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
        

@router.get(
    path='/groups/{group_id}/all',
    response_model=list[UserData]
)
def get_group_by_id(group_id: str, admin = Depends(get_keycloak_admin)):
    
    try:
        def get_subgroups(group_id: str, result: list[GroupData] = []) -> list[GroupData]:
            group = GroupData(**admin.get_group(group_id=group_id))
            result = group.subGroups
            for sg in group.subGroups:
                return result + get_subgroups(group_id=sg.id, result=result)
            return result
    
        subgroups = get_subgroups(group_id)
        return flatten(list(map(lambda sg: admin.get_group_members(group_id=sg.id), subgroups)))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
        