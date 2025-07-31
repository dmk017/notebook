import datetime
from typing import Optional

import pymongo
from returns.result import Result

from src.properties.properties_router_api_schema import PropertyListFilters
from src.database.collection_names import PROPERTIES_SCHEMA_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.properties.data.properties_schema import (PropertyPayload,
                                                            PropertySchema)
from src.utils.mongo import PydanticObjectId

properies_schemas_collection = get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME)


def add_property_schema(name: str, properties: list[PropertyPayload], user_id: str) -> PropertySchema:
    properties_schema = PropertySchema(
        name=name,
        properties=properties,
        next_id=None,
        owner_id=user_id
    )
    new_schema = properies_schemas_collection.insert_one(properties_schema.mongo())
    return PropertySchema.from_mongo(
        properies_schemas_collection.find_one({"_id": new_schema.inserted_id})
    )


def get_actual_properties_schema_by_name(name: str) -> Optional[PropertySchema]:
    actual_properties_schema = properies_schemas_collection.find(
        {"name": name}
    ).sort("_id", pymongo.DESCENDING).limit(1)
    actual_properties_schema = list(map(PropertySchema.from_mongo, actual_properties_schema))
    return actual_properties_schema[0] if len(actual_properties_schema) > 0 else None


def get_properties_by_name(name: str) -> list[PropertySchema]:
    result = properies_schemas_collection.find({"name": name}).sort("created_at", pymongo.DESCENDING)
    return list(map(PropertySchema.from_mongo, result))


def get_property_by_id(id: str) -> Optional[PropertySchema]:
    result = properies_schemas_collection.find_one({"_id": PydanticObjectId(id)})
    return PropertySchema.from_mongo(result) if result is not None else None


def get_actual_properties(filters: PropertyListFilters, page: int = 1, limit: int = 0) -> list[PropertySchema]:
    query = {'next_id': None}
    if filters.is_deleted is not None:
        query.update({ "deleted": filters.is_deleted})
    properties = properies_schemas_collection.find(query).sort("created_at", pymongo.ASCENDING)
    if limit:
        properties = properties.skip(limit * (page - 1)).limit(limit)
    return list(map(PropertySchema.from_mongo, properties))


def update_property_schema(id: str, updated_values: dict) -> Result(PropertySchema):
    result = properies_schemas_collection.update_one({"_id": PydanticObjectId(id)}, {'$set': updated_values})
    return get_property_by_id(id) if result.modified_count else None
