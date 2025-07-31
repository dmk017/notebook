from models.templates_models import add_model_template, get_models_template
from models.sends_models import (
    send_get_models_request,
    send_update_model_request,
    send_get_model_by_id_request,
)
from models.utils_models import (
    build_properties,
    build_properties_for_model,
    create_and_send_model_request,
)


def test_update_model(authenticated_client):
    properties = build_properties(
        authenticated_client,
        f"props_for_test_update_model",
        f"props_for_test_update_model",
    )
    model_data = create_and_send_model_request(
        authenticated_client, f"test_update_model", properties
    )

    request_body_get_model = get_models_template(
        name="test", is_deleted=False, is_actual=True
    )
    response_get_model = send_get_models_request(
        authenticated_client, request_body_get_model, page=1, limit=100
    )
    response_get_model_json = response_get_model.json()

    id_model = response_get_model_json["data"][0]["_id"]

    properties = build_properties(
        authenticated_client,
        f"props_for_test_update_model_new",
        f"props_for_test_update_model_new",
    )
    request_body = add_model_template(
        name="test_update_model", properties=build_properties_for_model(properties)
    )
    response_update = send_update_model_request(
        authenticated_client, request_body, id_model
    )
    response_update_json = response_update.json()
    next_id_update_model = response_update_json["_id"]

    response = send_get_model_by_id_request(
        authenticated_client, {}, next_id_update_model
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["_id"] == next_id_update_model
    assert response_json["name"] == "test_update_model"
    assert response_json["owner_id"] == response_get_model_json["data"][0]["owner_id"]
    assert response_json["deleted"] is False

    assert len(response_update_json["properties"]) == len(
        response_get_model_json["data"][-1]["properties"]
    )