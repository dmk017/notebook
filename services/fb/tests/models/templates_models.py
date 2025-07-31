def add_model_template(name="", properties=[]):
    return {"name": name, "properties": properties}


def get_models_template(name="", is_deleted=False, is_actual=True):
    return {"name": name, "is_deleted": is_deleted, "is_actual": is_actual}
