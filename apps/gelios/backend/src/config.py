import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = os.getenv("HOST")
    port: int = os.getenv("PORT")

    api_prefix: str = os.getenv("API_PREFIX")

    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_driver: str = "asyncpg"
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_port: str = os.getenv("POSTGRES_PORT")

    realm_name: str = os.getenv("REALM_NAME")
    kc_server_url: str = os.getenv("KC_SERVER_URL")
    kc_auth_server_url: str = os.getenv("KC_AUTH_SERVER_URL")

    client_id: str = os.getenv("CLIENT_ID")
    client_secret_key: str = os.getenv("CLIENT_SECRET_KEY")

    gelios_root_group_name: str = os.getenv("GELIOS_ROOT_GROUP_NAME")
    gelios_group_id: str = os.getenv("GELIOS_GROUP_ID")

    admin_cli_service_host: str = os.getenv("ADMIN_CLI_SERVICE_HOST")
    admin_cli_service_port: str = os.getenv("ADMIN_CLI_SERVICE_PORT")

    @property
    def db_host_uri(self):
        return f"postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    def get_user_info_uri(self, user_id: str):
        return f"http://{self.admin_cli_service_host}:{self.admin_cli_service_port}/api/v1/users/{user_id}"

    def get_subgroups_by_group_id(self):
        return f"http://{self.admin_cli_service_host}:{self.admin_cli_service_port}/api/v1/groups/{self.gelios_group_id}/all"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
