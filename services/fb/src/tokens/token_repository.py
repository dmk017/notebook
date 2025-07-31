from enum import Enum
from typing import Optional

import pymongo
from returns.result import Failure, Result, Success

from src.database.collection_names import TOKEN_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.tokens.token_schema import TokenSchema
from src.utils.mongo import PyObjectId

tokens_collection = get_collection_by_name(TOKEN_COLLECTION_NAME)


class AddTokenError(Enum):
    DUPLICATE_TOKEN_VALUE = "DUPLICATE_TOKEN_VALUE"


def add_token(user_id: str, value: str, access_model_kind_names: list[str]) -> Result[TokenSchema, AddTokenError]:
    token = TokenSchema(
        user_id=user_id,
        value=value,
        access_model_kind_names=access_model_kind_names
    )
    try:
        new_token = tokens_collection.insert_one(token.mongo())
    except pymongo.errors.DuplicateKeyError:
        return Failure(AddTokenError.DUPLICATE_TOKEN_VALUE)
    return Success(get_token_by_id(new_token.inserted_id))


def get_all_tokens_by_user_id(user_id: str) -> list[TokenSchema]:
    return list(map(TokenSchema.from_mongo, tokens_collection.find(
        {"user_id": user_id}).sort('created_at', pymongo.ASCENDING)))


def get_users_with_some_models_ids(access_model_kind_names: list[str]) -> list[str]:
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "access_model_kind_names": 1,
                "user_id": 1,
                "created_at": 1,
                "isExist": {"$gte": [
                    {
                        "$size": {
                            "$setIntersection": ['$access_model_kind_names', access_model_kind_names]
                        }
                    },
                    1
                ]},

            }
        },
        {
            "$match": {
                "isExist": True
            }
        },
        {
            "$group":
            {
                "_id": "$user_id",
                "maxCreatedAt": {"$max": "$created_at"},
            },
        },
    ]
    result = list(tokens_collection.aggregate(pipeline))
    user_ids = list(map(lambda item: item['_id'], result))
    return user_ids


def get_token_by_user_id(user_id: str) -> Optional[TokenSchema]:
    # Получаем послдений токен пользователя
    tokens = list(map(
        TokenSchema.from_mongo,
        tokens_collection.find(
            {"user_id": user_id}
        ).sort("_id", pymongo.DESCENDING).limit(1)
    ))
    return tokens[0] if tokens else None


def update_token(token_id, update_token_filter) -> Optional[TokenSchema]:
    update_token = tokens_collection.update_one(
        {"_id": PyObjectId(token_id)}, {"$set": update_token_filter}, upsert=False)
    if not update_token.modified_count:
        return None
    return get_token_by_id(token_id)


def get_token_by_id(id: str) -> Optional[TokenSchema]:
    return TokenSchema.from_mongo(tokens_collection.find_one({"_id": PyObjectId(id)}))
