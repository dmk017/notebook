import datetime
from typing import Generic, TypeVar, Union

import pymongo
from pydantic import ConfigDict, BaseModel, Field

from src.utils.types.UBaseModel import UBaseModel
from src.database.collection_names import OBJECTS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.types.primitive_type_enum import PrimitiveTypeEnum
from src.utils.mongo import MongoModel, PydanticObjectId


class ObjectStatus(BaseModel):
    approve_at: datetime.datetime| None = Field(default=None)
    decline_at: datetime.datetime | None = Field(default=None)
    reason: str | None = Field(default=None)
    moderator_id: str | None = Field(default=None)


TData = TypeVar("TData")
TType = TypeVar("TType")


class TPayloadValues(BaseModel, Generic[TData]):
    name: str = Field(...)
    values: list[TData]


class TPayloadData(TPayloadValues, Generic[TType, TData]):
    type: TType


StringPayloadData = TPayloadData[PrimitiveTypeEnum.STR.name, str]
NumberPayloadData = TPayloadData[PrimitiveTypeEnum.NUMBER.name, int]
DatePayloadData = TPayloadData[PrimitiveTypeEnum.DATE.name, datetime.datetime]
BoolPayloadData = TPayloadData[PrimitiveTypeEnum.BOOL.name, bool]
FilePayloadData = TPayloadData[PrimitiveTypeEnum.FILE.name, str]


class ObjectPropertyPayload(BaseModel):
    property_name: str
    data: list[TPayloadData]


ObjectPropertyPayloads = list[ObjectPropertyPayload]


class ObjectSchema(UBaseModel, MongoModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    status: ObjectStatus = Field(default=ObjectStatus())
    owner_id: str
    model_id: PydanticObjectId = Field(...)
    deleted: bool = Field(default=False)
    payload: ObjectPropertyPayloads = Field(...)
    model_config = ConfigDict(title=OBJECTS_COLLECTION_NAME)

PayloadData = Union[
    StringPayloadData,
    NumberPayloadData,
    DatePayloadData,
    BoolPayloadData,
    FilePayloadData
]

ObjectPropertyPayload.model_rebuild()

get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index("model_id")
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index("owner_id")
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index(
    [
        ("status.approve_at", pymongo.DESCENDING), ("status.decline_at", pymongo.DESCENDING)
    ]
)
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index(
    [
        ("$**", pymongo.TEXT)
    ]
)
