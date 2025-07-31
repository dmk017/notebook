from random import randint
from typing import Any, Callable, Dict, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from enum import Enum
import redis
from redis import Redis
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful
from keycloak import KeycloakOpenID
import requests
import time

from src.config import get_settings
from src.handlers.data.texts.get_texts import get_i18n_text

settings = get_settings()


keycloak_openid = KeycloakOpenID(
    server_url=settings.kc_auth_server_url + "/auth",
    client_id=settings.client_id,
    realm_name=settings.realm_name,
    client_secret_key=settings.client_secret_key,
    verify=True,
)

class TokenError(Enum):
    NOT_AUTHORIZED = "NOT_AUTHORIZED"
    TOKEN_IS_NOT_VALID = 'TOKEN_IS_NOT_VALID'

def fetch_jwks() -> Dict[str, Any]:
    jwks_response = requests.get(settings.kc_auth_server_url + "/realms/{0}".format(settings.realm_name))
    jwks: Dict[str, Any] = jwks_response.json()
    return jwks

def get_idp_public_key():
    try:
        return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{fetch_jwks()['public_key']}"
        "\n-----END PUBLIC KEY-----"
    )
    except Exception as e:
        print(e)

def get_payload(token: str) -> dict:
    try:
        key = get_idp_public_key()
        result = keycloak_openid.decode_token(
            token,
            key= key,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
        return result
    except Exception as e:
        print(e)

class CheckTokenMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, redis_connection_url: str, redis_port: int, redis_db: int, redis_keys_name: str):
        self.redis_client = Redis(host=redis_connection_url, port=redis_port, db=redis_db)
        self.bot = bot
        self.redis_keys_name = redis_keys_name

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id
        token = self.get_token_by_user_id(str(user_id))
        if not is_successful(token):
            auth_url = keycloak_openid.auth_url(
                settings.url_callback_keycloak, 'openid', state=user_id
            )
            html_link = '<a href="{0}">{1}</a>'.format(auth_url, get_i18n_text('texts.auth.link_text'))
            message = get_i18n_text('texts.auth.login_in') + html_link if token.failure() == TokenError.NOT_AUTHORIZED else get_i18n_text('texts.auth.refresh_token') + html_link
            await self.bot.send_message(
                user_id,
                message
            )
            return {"error": "Invalid access"}
        
        data['access_token'] = token.unwrap()

        return await handler(event, data)

    def get_token_by_user_id(self, user_id: str) -> Result[Any, TokenError]:
        access_token = self.redis_client.get("{0}:{1}".format(self.redis_keys_name, user_id))
        if access_token:
            payload = get_payload(access_token.decode('utf-8'))
            return Success(access_token.decode('utf-8')) if self.check_valid_token(payload) else Failure(TokenError.TOKEN_IS_NOT_VALID)
        
        return Failure(TokenError.NOT_AUTHORIZED)
        
    def check_valid_token(self, payload: dict) -> bool:
        return time.time() < payload["exp"]
    
    def __del__(self):
        self.redis_client.close()
