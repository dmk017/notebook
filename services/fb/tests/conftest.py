import pytest
import os
from fastapi import FastAPI
from src.exceptions_handler import exception_handlers
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from pymongo import MongoClient

from src.main import app, init_app, init_api_routers
from src.config import get_settings
from src.database.initiate_database import drop_collections, initiate_collections
from src.keycloak.keycloak_integration import get_user_info
from src.keycloak.keycloak_models import User
from src.keycloak.keycloak_integration import (
    get_user_info,
)


@pytest.fixture(scope="session")
def test_app():
    test_app = FastAPI(exception_handlers=exception_handlers)
    init_api_routers(test_app)
    yield test_app


@pytest.fixture(scope="session")
def client(test_app):
    test_mongo_connection_url = "mongodb://iojAF69cm6KAhzE:!Iea&TKX70n6QX0wiXSvryFth9KT@fortuna-mongo_db-1:27017/?retryWrites=true&w=majority"
    test_mongo_client = MongoClient(test_mongo_connection_url)
    initiate_collections(test_mongo_client, "fortuna_test")
    test_app.mongodb_client = test_mongo_client

    with TestClient(test_app) as client:
        yield client


@pytest.fixture(scope="session")
def authenticated_client(test_app, client):
    user = User(
        role="ADMIN", user_id="42ca4873-1229-4379-91c3-bb9704f57cab", user_name="test"
    )
    get_user_info_mock = MagicMock(return_value=user)
    test_app.dependency_overrides[get_user_info] = get_user_info_mock

    yield client

    test_app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db(test_app):
    yield
    
    drop_collections(test_app.mongodb_client, "fortuna_test")
    test_app.mongodb_client.close()