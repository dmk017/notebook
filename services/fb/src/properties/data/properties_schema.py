import datetime

from pydantic import ConfigDict, Field

from src.database.collection_names import PROPERTIES_SCHEMA_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.types.primitive_type_enum import PrimitiveTypeEnum
from src.utils.mongo import MongoModel, PydanticObjectId


class PropertyPayload(MongoModel):
    name: str = Field(...)
    primitive_type: PrimitiveTypeEnum = Field(...)
    help_text: str | None = Field(default=None)
    is_required: bool = Field(default=False)
    is_multiple: bool = Field(default=False)
    validation: str = Field(default="^.{2,}$")


class PropertySchema(MongoModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: str = Field(...)
    owner_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    # TODO: change name: properties -> primitives
    properties: list[PropertyPayload] = Field(...)
    next_id: PydanticObjectId | None = Field(...)
    deleted: bool = Field(default=False)
    model_config = ConfigDict(title=PROPERTIES_SCHEMA_COLLECTION_NAME)


get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME).create_index("name")
get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME).create_index("next_id")
