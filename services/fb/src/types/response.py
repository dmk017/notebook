import io
from typing import Generic, TypeVar
from fastapi import Response
from pydantic import BaseModel

from src.utils.str import normilize
from src.errors.errors import ErrorModel

TResponseType = TypeVar("TResponseType")


class ReponseError(BaseModel):
    code: ErrorModel
    details: str = ''


class TResponse(BaseModel, Generic[TResponseType]):
    success: bool
    message: str = ''
    data: TResponseType | None = None
    errors: list[ReponseError] = []


def buffer_file_response(buffer: io.BytesIO, filename: str, media_type: str) -> Response:
    headers = {
        'Content-Disposition': f"attachment; filename=\"{normilize.normilize(filename)}\""
    }
    return Response(
        buffer.getvalue(),
        headers=headers,
        media_type=media_type
    )
