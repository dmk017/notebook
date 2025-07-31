import io
from pydantic import BaseModel


class FileBufferContent(BaseModel):
    name: str
    buffer: io.BytesIO

    class Config:
        arbitrary_types_allowed = True
