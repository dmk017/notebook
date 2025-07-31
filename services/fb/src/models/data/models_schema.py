import datetime

from pydantic import ConfigDict, BaseModel, Field

from src.database.collection_names import MODELS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.mongo import MongoModel, PydanticObjectId


class ModelPropertyPayload(BaseModel):
    id: PydanticObjectId = Field(...)
    is_required: bool = Field(default=True)


class ModelSchema(MongoModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: str = Field(...)
    owner_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    properties: list[ModelPropertyPayload] = Field(...)
    next_id: PydanticObjectId | None = Field(...)
    deleted: bool = Field(default=False)
    model_config = ConfigDict(title=MODELS_COLLECTION_NAME)


get_collection_by_name(MODELS_COLLECTION_NAME).create_index("name")
