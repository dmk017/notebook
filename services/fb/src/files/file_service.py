import os

import bson

from src.config import get_settings
from src.libs.nextcloud_integration.NextCloudAPI import NextCloudAPI
from src.files.data import file_repository
from src.files.data.file_schema import FileSchema
from src.models.models_service import get_available_models_by_user_id

settings = get_settings()

nc = NextCloudAPI(
    instance=settings.next_cloud_uri,
    user=settings.next_cloud_user,
    password=settings.next_cloud_password
)


def add_file(
        user_id: str,
        model_id: str,
        file: list[bytes],
        conetnt_type: str,
        file_name: str
) -> FileSchema:
    file_id = bson.objectid.ObjectId()
    _, extension = os.path.splitext(file_name)
    response = nc.upload_file(
        file=file,
        content_type=conetnt_type,
        file_name=f"{file_id}{extension}"
    )
    if not response['success']:
        return None
    return file_repository.add_file(
        file_id=file_id,
        owner_id=user_id,
        model_id=model_id,
        path=response['data']['nc_path'],
        name=file_name,
        extension=extension,
        content_type=conetnt_type
    )


def get_file_by_id(
    file_id: str
) -> FileSchema:
    return file_repository.get_file_by_id(file_id)


def download_file(
    file_id: str,
    user_id: str,
    user_role: str
):
    file_info = file_repository.get_file_by_id(file_id)
    available_models_list = [str(schema.id)
                             for schema in get_available_models_by_user_id(user_id=user_id, user_role=user_role)]
    if str(file_info.model_id) not in available_models_list:
        return None
    return [file_info, nc.download_file(file_info.path)]
