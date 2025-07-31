from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings

from src import service


settings = get_settings()


def init_api_routers(app: FastAPI):
    app.include_router(service.router,
                       prefix=settings.api_prefix)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def init_app() -> FastAPI:
    app = FastAPI()
    init_api_routers(app)
    return app

app = init_app()
