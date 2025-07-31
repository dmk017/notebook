from typing import Optional

from returns.result import Failure, Result, Success

from src.errors.errors import Errors
from src.models import models_service
from src.models.data.models_schema import ModelPropertyPayload
from src.properties.data import properties_repository
from src.properties.data.properties_schema import (PropertyPayload,
                                                            PropertySchema)


def get_property_by_id(id: str) -> Optional[PropertySchema]:
    return properties_repository.get_property_by_id(id)


def get_property_history(id: str) -> list[PropertySchema]:
    property_data = properties_repository.get_property_by_id(id)
    return properties_repository.get_properties_by_name(property_data.name)


def get_actual_properties_schema_by_name(name: str) -> Optional[PropertySchema]:
    return properties_repository.get_actual_properties_schema_by_name(name)


def add_property(name: str,
                 properties: list[PropertyPayload],
                 user_id: str) -> Result[PropertySchema,
                                         Errors.PROPERTY_DUPLICATE_NAME_3001]:
    previous_version = properties_repository.get_actual_properties_schema_by_name(name)
    if previous_version:
        return Failure(Errors.PROPERTY_DUPLICATE_NAME_3001)
    return Success(properties_repository.add_property_schema(name, properties, user_id=user_id))


def update_property(name: str,
                    properties: list[PropertyPayload],
                    user_id: str) -> Result[PropertySchema,
                                            Errors.PROPERTY_NOT_FOUND_PREV_3002]:
    previous_version = properties_repository.get_actual_properties_schema_by_name(name)
    if not previous_version:
        return Failure(Errors.PROPERTY_NOT_FOUND_PREV_3002)
    previous_version_id = str(previous_version.id)
    actual_version_id = str(properties_repository.add_property_schema(name, properties, user_id=user_id).id)

    # обновляем пользовательский тип у каждой модели где он присутствовал
    models = models_service.get_models_by_property_ids([previous_version_id])
    for model in models:
        models_service.update_model(
            name=model.name,
            properties=[
                ModelPropertyPayload(
                    id=actual_version_id,
                    is_required=p.is_required
                ) if str(p.id) == previous_version_id else p for p in model.properties],
            user_id=model.owner_id)
    return Success(properties_repository.update_property_schema(previous_version_id, {'next_id': actual_version_id}))


def recove_delete_property(id: str, deleted: bool) -> Result[PropertySchema, Errors.PROPERTY_NOT_FOUND_3003]:
    properties = get_property_history(id)
    for property in properties: 
      properties_repository.update_property_schema(property.id, {"deleted": deleted})
    result = get_property_by_id(id)
    if result is None:
        return Failure(Errors.PROPERTY_NOT_FOUND_3003)
    return Success(result)
