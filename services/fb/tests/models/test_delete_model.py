from models.templates_models import get_models_template
from models.sends_models import send_get_models_request, send_delete_model_request
from models.utils_models import build_properties, create_and_send_model_request


def test_delete_model(authenticated_client):
    count = 2
    responses = []

    for i in range(count):
        properties = build_properties(
            authenticated_client,
            f"props_for_test_delete_model_{i}",
            f"props_for_test_delete_model_{i}",
        )
        model_data = create_and_send_model_request(
            authenticated_client, f"test_delete_model_{i}", properties
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

    response = send_delete_model_request(authenticated_client, {}, id_model)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["_id"] == id_model
    assert response_json["name"] == response_get_model_json["data"][0]["name"]
    assert response_json["owner_id"] == response_get_model_json["data"][0]["owner_id"]
    assert response_json["deleted"] is True

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
