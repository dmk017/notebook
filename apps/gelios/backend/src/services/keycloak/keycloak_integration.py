import requests
from typing import Optional
from keycloak import KeycloakOpenID
from src.config import get_settings
from fastapi import Security, HTTPException, status, Depends
from src.services.keycloak.OAuth2AuthCodeBearer import OAuth2AuthorizationCodeBearer
from src.services.keycloak.keycloak_models import (
    UserRole,
    GeliosRole,
    User,
    user_role_decoder_map,
)


settings = get_settings()


oauth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_server_url + "/protocol/openid-connect/auth",
    tokenUrl=settings.kc_auth_server_url + "/protocol/openid-connect/token",
)


keycloak_openid = KeycloakOpenID(
    server_url=settings.kc_server_url,
    client_id=settings.client_id,
    realm_name=settings.realm_name,
    client_secret_key=settings.client_secret_key,
    verify=True,
)


def fetch_jwks() -> dict[str, str | int]:
    jwks_response = requests.get(url=settings.kc_auth_server_url)
    return jwks_response.json()


async def get_idp_public_key():
    try:
        return (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{fetch_jwks()['public_key']}"
            "\n-----END PUBLIC KEY-----"
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Public key not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_payload(token: str = Security(oauth_scheme)) -> tuple[dict, str]:
    try:
        key = await get_idp_public_key()
        result = keycloak_openid.decode_token(
            token=token,
            key=key,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )
        return result, token
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_info(
    data: tuple[dict, str] = Depends(get_payload)
) -> tuple[User, str]:
    payload, token = data
    try:
        return (
            User(
                user_id=payload.get("sub"),
                user_name=payload.get("preferred_username"),
                role=get_gelios_role(user_roles=payload.get("realm_access")["roles"]),
            ),
            token,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_gelios_role(user_roles: list[str]) -> Optional[UserRole]:
    roles = [role.value for role in GeliosRole]
    for user_role in user_roles:
        if user_role in roles:
            return user_role_decoder_map[GeliosRole(user_role)]

    return
