from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from src.properties.data.properties_schema import PropertySchema
from src.models.data.models_schema import ModelSchema

class PropertiesPayload(BaseModel):
    id: str
    is_required: bool


class Payload(BaseModel):
    name: str
    properties: list[PropertiesPayload]


class AddModelRequest(BaseModel):
    payload: Payload


class ResponsePropertyPayload(BaseModel):
    payload: PropertySchema
    is_required: bool

class ResponseModel(ModelSchema):
    # TODO: сделать типы ответа и расширить из схем базы
    properties: list[ResponsePropertyPayload] = Field(...)

class ModelsListFilter(BaseModel):
    name: Optional[str] = None
    is_deleted: Optional[bool] = False
    is_actual: Optional[bool] = True