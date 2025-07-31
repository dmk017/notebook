import pytest

from models.templates_models import get_models_template
from models.sends_models import send_get_models_request, send_delete_model_request
from models.utils_models import build_properties, create_and_send_model_request


def test_get_models(authenticated_client):
    count = 2
    responses = []

    for i in range(count):
        properties = build_properties(
            authenticated_client,
            f"props_for_test_get_models_{i}",
            f"props_for_test_get_models_{i}",
        )
        model_data = create_and_send_model_request(
            authenticated_client, f"test_get_models_{i}", properties
        )
        responses.append(model_data)

    request_body = get_models_template(name="test", is_deleted=False, is_actual=True)
    response = send_get_models_request(
        authenticated_client, request_body, page=1, limit=100
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["page_number"] == 1
    for i, model_data in enumerate(response_json["data"][-2:0]):
        assert model_data["name"] == f"test_get_models"
        for j, payload in enumerate(model_data["properties"]):
            assert payload["payload"]["name"] == f"props_for_test_get_model_history_new_{i}"
            assert (
                payload["payload"]["properties"][0]["name"]
                == f"props_for_test_get_model_{i}_{j}"
            )


def test_get_models_with_invalid_limit(authenticated_client):
    request_body = get_models_template(name="test", is_deleted=False, is_actual=True)
    response = send_get_models_request(
        authenticated_client, request_body, page=1, limit=-1
    )

    assert response.status_code == 200
    assert response.json()["count"] == 10


def test_get_models_deleted_models_not_returned(authenticated_client):
    properties = build_properties(
        authenticated_client,
        "props_for_test_get_models_deleted",
        "props_for_test_get_models_deleted",
    )
    model_data = create_and_send_model_request(
        authenticated_client, "test_get_models_deleted", properties
    )

    send_delete_model_request(authenticated_client, {}, model_data["_id"])

    request_body = get_models_template(name="test", is_deleted=False, is_actual=True)
    response = send_get_models_request(
        authenticated_client, request_body, page=1, limit=10
    )
    response_json = response.json()

    assert response.status_code == 200
    assert model_data["_id"] not in [model["_id"] for model in response_json["data"]]
