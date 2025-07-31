from typing import Any
from pydantic import BaseModel, Field


class TPayloadValues(BaseModel):
    name: str = Field(...)
    values: list[Any]


class PropertyPayloadValues(BaseModel):
    property_name: str
    data: list[TPayloadValues]

class CountObjectsResposnse(BaseModel):
    total: int
  