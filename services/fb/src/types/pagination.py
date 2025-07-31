from typing import Generic, List, TypeVar

from pydantic import ConfigDict, BaseModel

from bson import ObjectId

T = TypeVar("T")


class ListRequest(BaseModel):
    page: int
    count: int


class ListResponse(BaseModel, Generic[T]):
    count: int
    page_number: int
    is_next: bool
    data: List[T]

    model_config = ConfigDict(json_serializer=lambda instance: {
        "count": instance.count,
        "page_number": instance.page_number,
        "is_next": instance.is_next,
        "data": [model.dict() for model in instance.data]
    })