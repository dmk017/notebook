from enum import Enum
from typing import Optional
from src.services.keycloak.keycloak_models import UserRole


class ChainAccess(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


def check_get_chains_list(
    owner_id: Optional[str], user_id: str, user_role: UserRole
) -> ChainAccess:
    if user_role == UserRole.ADMIN:
        return ChainAccess.ALLOW
    if owner_id == user_id:
        return ChainAccess.ALLOW

    return ChainAccess.DENY
