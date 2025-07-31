from pydantic import BaseModel
from enum import Enum

class UserRole(Enum):
    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'
    USER = 'USER'

class FortunaRole(Enum):
    ADMIN = 'fortuna_admin'
    MODERATOR = 'fortuna_moderator'
    USER = 'fortuna_user'

user_role_decoder_map: dict[FortunaRole, UserRole] = {
    FortunaRole.ADMIN: UserRole.ADMIN,
    FortunaRole.MODERATOR: UserRole.MODERATOR,
    FortunaRole.USER: UserRole.USER
}

class User(BaseModel):
    user_id: str
    user_name: str
    role: UserRole
