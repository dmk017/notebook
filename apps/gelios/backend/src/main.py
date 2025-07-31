import os
from fastapi import FastAPI
from src.config import get_settings
from src.database import Base, engine
from src.services.auth import auth_router
from src.services.users import users_router
from src.services.chain import chains_router
from src.services.server import servers_router
from fastapi.middleware.cors import CORSMiddleware
from src.workers.constants import TEMP_FOLDER_RELATIVE_PATH, DATA_FOLDER_RELATIVE_PATH


def init_router(_app: FastAPI) -> None:
    api_prefix = get_settings().api_prefix
    _app.include_router(servers_router.router, prefix=api_prefix)
    _app.include_router(chains_router.router, prefix=api_prefix)
    _app.include_router(users_router.router, prefix=api_prefix)
    _app.include_router(auth_router.router, prefix=api_prefix)


def init_database(_app: FastAPI) -> None:
    @_app.on_event("startup")
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


def init_middleware(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def prepare_dirs():
    dirs = [TEMP_FOLDER_RELATIVE_PATH, DATA_FOLDER_RELATIVE_PATH]
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)


def init_app() -> FastAPI:
    prepare_dirs()
    _app = FastAPI()
    init_middleware(_app)
    init_router(_app)
    init_database(_app)
    return _app


app = init_app()
