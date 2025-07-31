import datetime

import pymongo
from pydantic import Field

from src.database.collection_names import TOKEN_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.mongo import MongoModel, PyObjectId


class TokenSchema(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    value: str = Field(...)
    access_model_kind_names: list[str] = Field(...)
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    deprecated: bool = Field(default=False)


get_collection_by_name(TOKEN_COLLECTION_NAME).create_index([("user_id", pymongo.DESCENDING)])
get_collection_by_name(TOKEN_COLLECTION_NAME).create_index([("created_at", pymongo.DESCENDING)])
