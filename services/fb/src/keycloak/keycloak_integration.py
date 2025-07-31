from fastapi import Security, HTTPException, status, Depends
from keycloak import KeycloakOpenID
import requests
from typing import Any, Dict

from src.keycloak.OAuth2AuthCodeBearer import OAuth2AuthorizationCodeBearer
from src.config import get_settings
from src.keycloak.keycloak_models import User, FortunaRole, UserRole, user_role_decoder_map

settings = get_settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_server_url + "/protocol/openid-connect/auth",
    tokenUrl=settings.kc_auth_server_url + "/protocol/openid-connect/token",
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.kc_auth_server_url + "/protocol/openid-connect/auth",
    client_id=settings.client_id,
    realm_name=settings.realm_name,
    client_secret_key=settings.client_secret_key,
    verify=True
)

def fetch_jwks() -> Dict[str, Any]:
    jwks_response = requests.get(settings.kc_auth_server_url)
    jwks: Dict[str, Any] = jwks_response.json()
    return jwks

async def get_idp_public_key():
    try:
        return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{fetch_jwks()['public_key']}"
        "\n-----END PUBLIC KEY-----"
    )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Public key not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_payload(token: str = Security(oauth2_scheme)) -> tuple:
    try:
        key = await get_idp_public_key()
        result = keycloak_openid.decode_token(
            token,
            key=key,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )

        return result, token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_user_info(payload: tuple = Depends(get_payload)) -> User:
    result, _ = payload
    try:
        return User(
            user_id=result.get("sub"),
            user_name=result.get("preferred_username"),
            role=get_fortuna_role(result.get("realm_access")["roles"])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ERROR: can't create auth User object with error `{str(e)}`",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_user_token(payload: tuple = Depends(get_payload)) -> str:
    _, token = payload
    return token

def is_fortuna_role(role: str) -> bool:
    try:
        FortunaRole(role)
        return True
    except ValueError:
        return False
    
def get_fortuna_role(roles: list) -> UserRole:
    for role in roles:
        if is_fortuna_role(role):
            return user_role_decoder_map[FortunaRole(role)]
