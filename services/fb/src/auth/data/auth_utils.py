from src.models.data.models_repository import get_actual_model_by_name

def check_exist_model(access_model_names: list[str]) -> bool:
    return all(get_actual_model_by_name(model_name) is not None for model_name in access_model_names)