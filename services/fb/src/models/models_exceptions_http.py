from fastapi import HTTPException, status

from src.errors.errors import Errors


def models_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.MODEL_DUPLICATE_NAME_4001:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.MODEL_NOT_FOUND_PREV_4002:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
        case Errors.MODEL_NOT_FOUND_4003:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
