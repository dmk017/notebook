from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database.initiate_database import initiate_database
from src.exceptions_handler import exception_handlers

from src.files import file_router
from src.models import models_router_api
from src.objects import objects_router_api
from src.properties import properties_router_api
from src.auth.data import auth_router_api


settings = get_settings()


def init_db(_app: FastAPI):
    @_app.on_event("startup")
    def startup_db_client():
        app.mongodb_client = initiate_database()

    @_app.on_event("shutdown")
    def shutdown_db_client():
        app.mongodb_client.close()


def init_api_routers(app: FastAPI):
    app.include_router(properties_router_api.router,
                       prefix=settings.api_prefix)
    app.include_router(models_router_api.router,
                       prefix=settings.api_prefix)
    app.include_router(objects_router_api.router, prefix=settings.api_prefix)

    app.include_router(file_router.router, prefix=settings.api_prefix)

    app.include_router(auth_router_api.router, prefix=settings.api_prefix)

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])




def init_app() -> FastAPI:
    app = FastAPI(exception_handlers=exception_handlers)
    init_api_routers(app)
    init_db(app)
    return app


app = init_app()
