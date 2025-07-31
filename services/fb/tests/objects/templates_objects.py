def add_object_template(model_id, properties):
    return {"model_id": model_id, "properties": properties}


def approve_objects_template(
    objects_ids,
):
    return {
        "objectsId": objects_ids,
    }


def approve_objects_filters_template(filters):
    return {"filters": filters}


def decline_objects_template(
    objects_ids,
):
    return {
        "objectsId": objects_ids,
    }


def decline_objects_filters_template(filters):
    return {"filters": filters}


def search_objects_template(text, filters):
    return {"text": text, "page": 1, "count": 20, "filters": filters}


def unloading_objects_template(text, filters):
    return {"text": text, "page": 1, "count": 20, "filters": filters}
