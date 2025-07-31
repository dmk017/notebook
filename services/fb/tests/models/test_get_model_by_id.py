from models.templates_models import get_models_template
from models.sends_models import (
    send_get_models_request,
    send_get_model_by_id_request,
    send_delete_model_request,
)
from models.utils_models import build_properties, create_and_send_model_request


def test_get_model_by_id(authenticated_client):
    count = 2
    responses = []

    for i in range(count):
        properties = build_properties(
            authenticated_client,
            f"props_for_test_get_model_by_id_{i}",
            f"props_for_test_get_model_by_id_{i}",
        )
        model_data = create_and_send_model_request(
            authenticated_client, f"test_get_model_by_id_{i}", properties
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

    response = send_get_model_by_id_request(authenticated_client, {}, id_model)
    response_json = response.json()

    assert response.status_code == 200
    assert id_model == response_json["_id"]
    assert response_get_model_json["data"][0]["name"] == response_json["name"]
    assert len(response_get_model_json["data"][0]["properties"]) == len(
        response_json["properties"]
    )
    for j, payload in enumerate(response_json["properties"]):
        assert (
            payload["payload"]["name"]
            == response_get_model_json["data"][0]["properties"][j]["payload"]["name"]
        )
        assert (
            payload["payload"]["properties"][0]["name"]
            == response_get_model_json["data"][0]["properties"][j]["payload"][
                "properties"
            ][0]["name"]
        )


def test_get_deleted_model_by_id(authenticated_client):
    count = 2
    responses = []

    for i in range(count):
        properties = build_properties(
            authenticated_client,
            f"props_for_test_get_deleted_model_by_id_{i}",
            f"props_for_test_get_deleted_model_by_id_{i}",
        )
        model_data = create_and_send_model_request(
            authenticated_client, f"test_get_deleted_model_by_id_{i}", properties
        )
        responses.append(model_data)

    request_body_get_model = get_models_template(
        name="test", is_deleted=False, is_actual=True
    )
    response_get_model_before = send_get_models_request(
        authenticated_client, request_body_get_model, page=1, limit=100
    )
    response_get_model_before_json = response_get_model_before.json()
    id_model = response_get_model_before_json["data"][0]["_id"]

    response_delete = send_delete_model_request(authenticated_client, {}, id_model)
    response_delete_json = response_delete.json()

    response_get_model_after = send_get_models_request(
        authenticated_client, request_body_get_model, page=1, limit=100
    )
    response_get_model_after_json = response_get_model_after.json()

    response = send_get_model_by_id_request(authenticated_client, {}, id_model)
    response_json = response.json()

    assert response.status_code == 200
    assert (response_get_model_after_json["count"] + 1) == response_get_model_before_json["count"]
    assert id_model == response_json["_id"]

    assert response_get_model_before_json["data"][0]["name"] == response_json["name"]
    assert (
        response_get_model_before_json["data"][0]["deleted"] != response_json["deleted"]
    )
    assert len(response_get_model_before_json["data"][0]["properties"]) == len(
        response_json["properties"]
    )
    for j, payload in enumerate(response_json["properties"]):
        assert (
            payload["payload"]["name"]
            == response_get_model_before_json["data"][0]["properties"][j]["payload"][
                "name"
            ]
        )
        assert (
            payload["payload"]["properties"][0]["name"]
            == response_get_model_before_json["data"][0]["properties"][j]["payload"][
                "properties"
            ][0]["name"]
        )
