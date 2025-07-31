from pydantic import ConfigDict, Field
from typing import Literal
from enum import Enum

from pydantic import BaseModel, Field

from src.database.collection_names import AUTH_COLLECTION_NAME, AUTH_HISTORY_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.mongo import MongoModel, PydanticObjectId
from src.errors.errors import ErrorModel

import datetime

class AuthSchema(MongoModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    user_id: str = Field(...)
    user_name: str = Field(...)
    access_model_names: list[str] = Field(default=[])
    model_config = ConfigDict(title=AUTH_COLLECTION_NAME)


class AuthHistoryAccessModelSchema(MongoModel):
    user_id: str = Field(...)
    owner_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    payload: list[str] = Field(...)
    model_config = ConfigDict(title=AUTH_HISTORY_COLLECTION_NAME)

class ChangeAccessModelsSchema(BaseModel):
    user_id: str = Field(...)
    access_model_names: list[str] = Field(...)

class AuthErrors(Enum):
    ACCESS_DENIED = ErrorModel(message="ACCESS_DENIED", code=403)
    INVALID_SERVER = ErrorModel(message='INVALID_SERVER', code=500)


get_collection_by_name(AUTH_COLLECTION_NAME).create_index("user_id")