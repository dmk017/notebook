from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='./.env',
        env_file_encoding='utf-8'
    )

    bot_token: SecretStr
    url_api: str

    redis_connection_url: str
    redis_port: int
    redis_keys_name: str
    redis_chanel_name: str
    
    port: int
    host: str

    client_id: str
    realm_name: str
    client_secret_key: str
    kc_auth_server_url: str
    url_callback_keycloak: str


def get_settings() -> Settings:
    settings = Settings()

    return settings
