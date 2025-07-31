from fastapi import (APIRouter, HTTPException, Request, Response, UploadFile,
                     status, Depends)
from starlette.authentication import requires
from src.keycloak.keycloak_integration import get_user_info
from src.keycloak.keycloak_models import User
from src.files import file_service
from src.files.data.file_schema import FileSchema

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.post(
    path="/",
    response_model=FileSchema
)
async def upload_file(file: UploadFile, model_id: str, user: User = Depends(get_user_info)):
    result = file_service.add_file(
        user_id=user.user_id,
        model_id=model_id,
        file=(await file.read()),
        conetnt_type=file.content_type,
        file_name=file.filename
    )
    if result is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Is not able to upload file")
    return result


@router.get(
    path="/{file_id}"
)
async def download_file(file_id: str, user: User = Depends(get_user_info)):
    result = file_service.download_file(file_id, user_id=user.user_id, user_role=user.role.value)
    if result is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    [file_info, file_binary] = result
    return Response(content=file_binary, media_type=file_info.type)
