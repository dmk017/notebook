import datetime

from pydantic import ConfigDict, Field

from src.utils.types.UBaseModel import UBaseModel
from src.database.collection_names import FILES_COLLECTION_NAME
from src.utils.mongo import MongoModel, PydanticObjectId


class FileSchema(UBaseModel, MongoModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    model_id: str = Field(...)
    owner_id: str = Field(...)
    path: str = Field(...)
    original_name: str = Field(...)
    extension: str = Field(...)
    type: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    model_config = ConfigDict(title=FILES_COLLECTION_NAME)
