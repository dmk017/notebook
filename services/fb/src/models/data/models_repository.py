from typing import Optional

import pymongo

from src.models.models_router_api_schema import ModelsListFilter
from src.database.collection_names import MODELS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.models.data.models_schema import (ModelPropertyPayload,
                                                  ModelSchema)
from src.utils.mongo import PydanticObjectId

models_collection = get_collection_by_name(MODELS_COLLECTION_NAME)


def add_model(name: str, properties: list[ModelPropertyPayload], user_id: str) -> Optional[ModelSchema]:
    model = ModelSchema(
        name=name,
        properties=properties,
        owner_id=user_id,
        next_id=None
    )
    new_model = models_collection.insert_one(model.mongo())
    return get_model_by_id(new_model.inserted_id)


def get_actual_model_by_name(name: str) -> Optional[ModelSchema]:
    actual_model = models_collection.find({"name": name}).sort("_id", pymongo.DESCENDING).limit(1)
    actual_model = list(map(ModelSchema.from_mongo, actual_model))
    return actual_model[0] if len(actual_model) > 0 else None


def get_models_by_name(name: str) -> list[ModelSchema]:
    models = models_collection.find({"name": name}).sort("created_at", pymongo.DESCENDING)
    return list(map(ModelSchema.from_mongo, models))


def get_models_by_property_ids(property_ids: list[str]) -> list[ModelSchema]:
    filter_q = {"properties.id": {'$in': list(map(PydanticObjectId, property_ids))}}
    models = models_collection.find(filter_q)
    return list(map(ModelSchema.from_mongo, models))


def get_model_by_id(id: str) -> Optional[ModelSchema]:
    model = models_collection.find_one({"_id": PydanticObjectId(id)})
    return ModelSchema.from_mongo(model) if model is not None else None


def update_model(id: str, updated_values: dict) -> Optional[ModelSchema]:
    result = models_collection.update_one({'_id': PydanticObjectId(id)}, {'$set': updated_values})
    return get_model_by_id(id) if result.matched_count else None


def get_models(page: int, limit: int, filters: ModelsListFilter = ModelsListFilter(), available_models_id: list[str] = []) -> list[ModelSchema]:
    query = {}
    if filters.is_actual:
      query = { 'next_id': None }
    if filters.is_deleted is not None:
        query.update({ "deleted": filters.is_deleted })
    if len(available_models_id) > 0:
        query.update({ "_id": {'$in': list(map(PydanticObjectId, available_models_id))} })
    models = models_collection.find(query).sort(
        "name", pymongo.ASCENDING).skip(limit * (page - 1)).limit(limit)
    return list(map(ModelSchema.from_mongo, models))

