from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='./.env',
        env_file_encoding='utf-8'
    )

    redis_connection_url: str
    redis_port: int
    redis_keys_name: str
    redis_chanel_name: str
    
    port_auth: int
    host: str

    client_id: str
    realm_name: str
    client_secret_key: str
    kc_auth_server_url: str

    bot_url: str
    fb_bot_auth_url: str


def get_settings() -> Settings:
    settings = Settings()

    return settings