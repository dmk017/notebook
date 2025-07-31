from fastapi import HTTPException, status

from src.errors.errors import Errors


def objects_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.OBJECT_ADD_REQUEST_MALFORMED_5001:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.OBJECT_ADD_REQUEST_MALFORMED_5002:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.OBJECT_ADD_REQUEST_MALFORMED_5003:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.OBJECT_ADD_REQUEST_MALFORMED_5004:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
