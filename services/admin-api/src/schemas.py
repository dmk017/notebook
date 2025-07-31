from typing import Optional
from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    username: str
    firstName: str
    lastName: str
    email: str


class GroupData(BaseModel):
    id: str
    name: str
    path: str
    parentId: Optional[str] = None
    subGroups: list['GroupData']
    # members: list[UserData] = []