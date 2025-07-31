from datetime import datetime
from typing import Optional, Any, Literal, Union

from pydantic import BaseModel, Field

from src.utils.types.UBaseModel import UBaseModel
from src.objects.data.objects_schema import ObjectStatus
from src.objects.objects_service_schema import PropertyPayloadValues
from src.types.pagination import ListRequest
from src.types.response import TResponse
from src.utils.mongo import PydanticObjectId


class Payload(UBaseModel):
    model_id: str
    properties: list[PropertyPayloadValues]


class AddObjectRequest(BaseModel):
    payload: Payload


class Object(UBaseModel):
    id: PydanticObjectId
    created_at: datetime
    status: ObjectStatus
    owner_id: str
    model_id: str
    payload: Optional[list[PropertyPayloadValues]] = []


class ObjectDt(Object):
    model_name: str


class ObjectDtResponse(BaseModel):
    data: list[ObjectDt]
    draw: int
    recordsTotal: int
    recordsFiltered: int | None = None


class GetObjectsRequest(ListRequest):
    text: str

class SearchFilter(BaseModel):
    type: Literal['isolated']
    property: str = Field(..., description="Характеристика", examples=["status"])
    operator: str = Field(..., description="Оператор для запроса", examples=["eq"])
    value: Any = Field(...)

class SearchFiltersList(BaseModel):
    type: Literal['group']
    group: Union[Literal["OR", "AND"], None] = Field(None)
    conditions: list[Union[SearchFilter, 'SearchFiltersList']] = Field(...)

class SearchObject(BaseModel):
    text: str = Field(default="")
    page: int = Field(default=1)
    count: int = Field(default=10)
    filters: list[SearchFiltersList]


class ApproveDeclineShem(BaseModel):
    objectsId: list[str] | None = None
    filters: list[SearchFiltersList] | None = None
    reason: str | None = None

AddObjectResponse = TResponse[Object]
