import sys
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_ARG = 'dev'
DEBUG_MODE = sys.argv[0][len(sys.argv[0]) - len(DEV_ARG):] == DEV_ARG


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env.local',
        env_file_encoding='utf-8'
    )
    
    host: str
    port: int

    api_prefix: str

    mongo_db: str
    mongo_connection_url: str

    file_templates_path: str
    file_templates_header_delimeter: str
    file_templates_data_delimeter: str
    file_encoding: str

    next_cloud_uri: str
    next_cloud_user: str
    next_cloud_password: str

    client_id: str
    realm_name: str
    client_secret_key: str
    kc_auth_server_url: str


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings
