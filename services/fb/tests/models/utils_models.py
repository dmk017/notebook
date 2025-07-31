from models.templates_models import add_model_template
from models.sends_models import send_add_model_request, send_get_models_request
from properties.test_add_property import add_property


def build_properties(client, name, prop_name):
    count = 5
    properties = []

    for i in range(count):
        response = add_property(client, f"{name}_{i}", f"{prop_name}_{i}")
        properties.append(response.json())

    return properties


def build_properties_for_model(properties):
    properties_for_model = []

    for property in properties:
        properties_for_model.append(
            {
                "id": property["_id"],
                "is_required": property["properties"][0]["is_required"],
            }
        )

    return properties_for_model


def create_and_send_model_request(client, name, properties):
    request_body = add_model_template(
        name=name, properties=build_properties_for_model(properties)
    )
    response = send_add_model_request(client, request_body)
    return response.json()


def get_model_id_from_list_request(client, request_body, page, limit):
    response = send_get_models_request(client, request_body, page, limit)
    response_json = response.json()
    return response_json["data"]["_id"]
