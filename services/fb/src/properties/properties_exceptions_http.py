from fastapi import HTTPException, status

from src.errors.errors import Errors


def properties_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.PROPERTY_DUPLICATE_NAME_3001:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.PROPERTY_NOT_FOUND_PREV_3002:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.PROPERTY_NOT_FOUND_3003:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
