from enum import Enum
from pydantic import BaseModel


class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class GeliosRole(Enum):
    ADMIN = "gelios_admin"
    USER = "gelios_user"


user_role_decoder_map: dict[GeliosRole, UserRole] = {
    GeliosRole.ADMIN: UserRole.ADMIN,
    GeliosRole.USER: UserRole.USER,
}


class User(BaseModel):
    user_id: str
    user_name: str
    role: UserRole
