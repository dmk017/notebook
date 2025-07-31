from typing import Optional
from pydantic import BaseModel

from src.properties.data.properties_schema import PropertyPayload


class Payload(BaseModel):
    name: str
    properties: list[PropertyPayload]


class AddPropertySchemaRequest(BaseModel):
    payload: Payload

class PropertyListFilters(BaseModel):
    name: Optional[str] = None
    is_deleted: Optional[bool] = False
