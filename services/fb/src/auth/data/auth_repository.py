from typing import Optional

from src.auth.data.auth_schema import AuthSchema
from src.database.collection_names import AUTH_COLLECTION_NAME, AUTH_HISTORY_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.mongo import PydanticObjectId

auth_schemas_collection = get_collection_by_name(AUTH_COLLECTION_NAME)
auth_history_schemas_collection = get_collection_by_name(AUTH_HISTORY_COLLECTION_NAME)

def get_auth_user_by_id(user_id: str, user_name: str="") -> Optional[AuthSchema]:
    result = auth_schemas_collection.find_one({"user_id": user_id})
    # if result is None and user_name == "":
    #     return None
    if result is None:
        return add_user(user_id, user_name)
    return AuthSchema.from_mongo(result)


def add_user(user_id: str, user_name: str) -> Optional[AuthSchema]:
    add_schemas = AuthSchema(user_id=user_id, user_name=user_name, access_model_names=[])
    new_schema = auth_schemas_collection.insert_one(add_schemas.mongo())
    return AuthSchema.from_mongo(
        auth_schemas_collection.find_one({"_id": new_schema.inserted_id})
    )

def update_access_model_names(user_id: str, owner_id: str, access_model_names: list[str]) -> Optional[AuthSchema]:
    result = auth_schemas_collection.update_one({'user_id': user_id}, {'$set': {'access_model_names': access_model_names}})
    auth_history_schemas_collection.insert_one({ 'user_id': user_id, 'owner_id': owner_id, 'payload': access_model_names })
    return get_auth_user_by_id(user_id) if result.matched_count else None