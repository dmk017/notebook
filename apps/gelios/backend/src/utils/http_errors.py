from .errors import Errors
from fastapi import HTTPException, status


def fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.SERVER_IS_NOT_EXIST:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Errors.SERVER_IS_NOT_EXIST.value,
            )

        case Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION.value,
            )

        case Errors.SERVER_IS_NOT_AVAILABLE_FOR_WORKING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.SERVER_IS_NOT_AVAILABLE_FOR_WORKING.value,
            )

        case Errors.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.PERMISSION_DENIED.value,
            )

        case Errors.USER_IS_NOT_EXIST:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Errors.USER_IS_NOT_EXIST.value,
            )

        case Errors.CHAIN_IS_NOT_EXIST:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Errors.CHAIN_IS_NOT_EXIST.value,
            )

        case Errors.CHAIN_IS_NOT_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.CHAIN_IS_NOT_AVAILABLE.value,
            )

        case Errors.WRONG_CHOICE_OF_SERVERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.WRONG_CHOICE_OF_SERVERS.value,
            )

        case Errors.CHAIN_CLIENT_IS_NOT_EXIST:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Errors.CHAIN_CLIENT_IS_NOT_EXIST.value,
            )
