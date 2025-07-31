import re
from typing import Any, Optional

import pymongo
from fastapi.encoders import jsonable_encoder

from src.database.collection_names import OBJECTS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.objects.conversion_types_map.datetime_decoder import \
    dateime_decoder
from src.objects.data.objects_schema import (ObjectPropertyPayloads,
                                                    ObjectSchema, ObjectStatus)
from src.utils.mongo import PydanticObjectId
from src.utils.types_decoder import decode_to_primitive_type

objects_collection = get_collection_by_name(OBJECTS_COLLECTION_NAME)


def add_object(owner_id: str, model_id: str, payload: ObjectPropertyPayloads) -> ObjectSchema:
    object = ObjectSchema(
        owner_id=owner_id,
        model_id=model_id,
        payload=payload
    )
    new_object = objects_collection.insert_one(object.mongo())
    return get_object_by_id(new_object.inserted_id)


def get_object_by_id(id: str) -> Optional[ObjectSchema]:
    object = objects_collection.find_one({"_id": PydanticObjectId(id)})
    return ObjectSchema.from_mongo(object) if object is not None else None


def update_many_objects(ids: list[PydanticObjectId], status: ObjectStatus):
    return objects_collection.update_many(
        {'_id': {'$in': ids}},
        {'$set': {
            'status': jsonable_encoder(status)
        }}
    ).modified_count


def get_objects(
    page: int,
    limit: int,
    filtersOr: dict[str, Any],
    filtersAnd: dict[str, Any],
    model_ids: list[str],
    text: str
):
    query = get_query_objects(
        filtersOr=filtersOr,
        filtersAnd=filtersAnd,
        model_ids=list(map(PydanticObjectId, model_ids)),
        text=text
    )
    objects = objects_collection \
        .find(query) \
        .sort("created_at", pymongo.DESCENDING) \
        .skip((page - 1) * limit) \
        .limit(limit)
    return list(map(ObjectSchema.from_mongo, objects))


def get_objects_count(
    filtersOr: dict[str, Any],
    filtersAnd: dict[str, Any],
    model_ids: list[str],
    text: str
):
    query = get_query_objects(
        filtersOr=filtersOr,
        filtersAnd=filtersAnd,
        model_ids=list(map(PydanticObjectId, model_ids)),
        text=text
    )
    return objects_collection.count_documents(query)


def get_query_objects(
    filtersOr: dict[str, Any],
    filtersAnd: dict[str, Any],
    model_ids: list[str],
    text: str
):
    query = {}
    if text:
        query["$text"] = {"$search": text}
    if filtersOr:
        query["$or"] = filtersOr['$or']
    if filtersAnd:
        query["$and"] = filtersAnd['$and']
    if model_ids:
        model_ids_filter = {
            "model_id": {"$in": model_ids}
        }
        query["$and"] = [*query.get("$and", []), model_ids_filter]
    return query


def to_regex_query(value):
    def fnPattern(value):
        return re.compile(rf'.*{value}.*', re.I | re.S)
    value = decode_to_primitive_type(value.lower())
    return {'$regex': fnPattern(value)}


def decode_to_status_filter(value):
    if value == 'approved':
        return [{"$ne": None}, {"$eq": None}]
    elif value == 'declined':
        return [{"$eq": None}, {"$ne": None}]
    elif value == 'waiting':
        return [{"$eq": None}, {"$eq": None}]
