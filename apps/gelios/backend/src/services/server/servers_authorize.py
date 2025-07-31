from enum import Enum
from typing import Optional
from src.services.keycloak.keycloak_models import UserRole


class ServerAccess(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


def check_get_servers_list(
    owner_id: Optional[str], user_id: str, user_role: UserRole
) -> ServerAccess:
    if user_role == UserRole.ADMIN:
        return ServerAccess.ALLOW
    if owner_id == user_id:
        return ServerAccess.ALLOW

    return ServerAccess.DENY
