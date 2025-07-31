from fastapi import FastAPI

from src.database.init_database import initiate_database
from src.auth.auth_router import router

def init_db(_app: FastAPI):
    @_app.on_event("startup")
    def startup_db_client():
        app.redis_client = initiate_database()

    @_app.on_event("shutdown")
    def shutdown_db_client():
        app.redis_client.close()

def init_api_routers(app: FastAPI):
    app.include_router(router)



def init_app() -> FastAPI:
    app = FastAPI()
    init_api_routers(app)
    init_db(app)
    return app


app = init_app()