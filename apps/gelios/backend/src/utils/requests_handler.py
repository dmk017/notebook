import requests
from typing import Optional
from pydantic import BaseModel
from src.config import get_settings
from src.services.server.servers_router_schema import UserData


class GroupMembers(BaseModel):
    users: list[UserData]
    count: int


settings = get_settings()


def get_user_info_by_user_id(token: str, owner_id: str) -> Optional[UserData]:
    response = requests.get(
        url=settings.get_user_info_uri(user_id=owner_id),
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.ok:
        user_data = response.json()
        return UserData(
            id=user_data.get("id"),
            username=user_data.get("username"),
            first_name=user_data.get("firstName"),
            last_name=user_data.get("lastName"),
        )
    return


def get_group_members(token: str):
    response = requests.get(
        url=settings.get_subgroups_by_group_id(),
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    return GroupMembers(
        count=len(data),
        users=[
            UserData(
                id=user.get("id"),
                username=user.get("username"),
                first_name=user.get("firstName"),
                last_name=user.get("lastName"),
            )
            for user in data
        ],
    )
