from src.database.collection_names import FILES_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.files.data.file_schema import FileSchema
from src.utils.mongo import PydanticObjectId

files_collection = get_collection_by_name(FILES_COLLECTION_NAME)


def get_file_by_id(id: str) -> FileSchema:
    object = files_collection.find_one({"_id": PydanticObjectId(id)})
    return FileSchema.from_mongo(object) if object is not None else None


def add_file(
        file_id: str,
        owner_id: str,
        model_id: str,
        path: str,
        name: str,
        extension: str,
        content_type: str) -> FileSchema:
    object = FileSchema(
        id=file_id,
        owner_id=owner_id,
        model_id=model_id,
        path=path,
        original_name=name,
        extension=extension,
        type=content_type
    )
    new_object = files_collection.insert_one(object.mongo())
    return get_file_by_id(new_object.inserted_id)
