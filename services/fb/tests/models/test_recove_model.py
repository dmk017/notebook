from models.templates_models import get_models_template
from models.sends_models import (
    send_get_models_request,
    send_delete_model_request,
    send_get_recove_model_request,
)
from models.utils_models import build_properties, create_and_send_model_request


def test_recove_model(authenticated_client):
    count = 2
    responses = []

    for i in range(count):
        properties = build_properties(
            authenticated_client,
            f"props_for_test_recove_model_{i}",
            f"props_for_test_recove_model_{i}",
        )
        model_data = create_and_send_model_request(
            authenticated_client, f"test_recove_model_{i}", properties
        )
        responses.append(model_data)

    request_body_get_model = get_models_template(
        name="test", is_deleted=False, is_actual=True
    )
    response_get_model = send_get_models_request(
        authenticated_client, request_body_get_model, page=1, limit=10
    )
    response_get_model_json = response_get_model.json()

    id_model = response_get_model_json["data"][0]["_id"]

    assert response_get_model_json["data"][0]["deleted"] == False

    response_delete = send_delete_model_request(authenticated_client, {}, id_model)
    response_delete_json = response_delete.json()

    assert response_delete_json["deleted"] == True

    response = send_get_recove_model_request(authenticated_client, {}, id_model)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["_id"] == id_model
    assert response_json["name"] == response_get_model_json["data"][0]["name"]
    assert response_json["owner_id"] == response_get_model_json["data"][0]["owner_id"]
    assert response_json["deleted"] is False

    assert len(response_get_model_json["data"][0]["properties"]) == len(
        response_json["properties"]
    )
    for j, payload in enumerate(response_json["properties"]):
        assert (
            payload["id"]
            == response_get_model_json["data"][0]["properties"][j]["payload"]["_id"]
        )
        assert (
            payload["is_required"]
            == response_get_model_json["data"][0]["properties"][j]["is_required"]
        )


def test_recove_model_not_deleted(authenticated_client):
    properties = build_properties(
        authenticated_client,
        "props_for_test_recove_model_not_deleted",
        "props_for_test_recove_model_not_deleted",
    )
    model_data = create_and_send_model_request(
        authenticated_client, "test_recove_model_not_deleted", properties
    )
    model_id = model_data["_id"]

    response = send_get_recove_model_request(authenticated_client, {}, model_id)
    response_json = response.json()

    assert response.status_code == 200
    assert model_data == response_json
