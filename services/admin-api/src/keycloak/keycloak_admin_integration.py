from fastapi import Security, HTTPException, status, Depends
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection
import requests
from typing import Any, Dict

from src.keycloak.OAuth2AuthCodeBearer import OAuth2AuthorizationCodeBearer
from src.config import get_settings
from src.keycloak.keycloak_models import User

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

async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        key = await get_idp_public_key()
        return keycloak_openid.decode_token(
            token,
            key=key,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_keycloak_admin(payload: dict = Depends(get_payload)) -> User:
    try:
        roles = payload.get("resource_access")["realm-management"]["roles"]
        if 'view-users' not in roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not allowed. Not found access role",
                headers={"WWW-Authenticate": "Bearer"},
            )
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=settings.kc_server_url,
            realm_name=settings.realm_name,
            client_id=settings.client_id,
            username=settings.manager_username,
            password=settings.manager_password,
            verify=True
        )
        return KeycloakAdmin(connection=keycloak_connection)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )