from models.templates_models import add_model_template
from models.sends_models import (
    send_update_model_request,
    send_get_model_history_request,
    send_delete_model_request,
)
from models.utils_models import (
    build_properties,
    build_properties_for_model,
    create_and_send_model_request,
)


def test_get_model_history(authenticated_client):
    properties = build_properties(
        authenticated_client,
        "props_for_test_get_model_history",
        "props_for_test_get_model_history",
    )
    model_data = create_and_send_model_request(
        authenticated_client, "test_get_model_history", properties
    )
    model_id = model_data["_id"]

    updated_properties = build_properties(
        authenticated_client,
        "props_for_test_get_model_history_new",
        "props_for_test_get_model_history_new",
    )
    request_body_update = add_model_template(
        name="test_get_model_history",
        properties=build_properties_for_model(updated_properties),
    )
    response_update = send_update_model_request(
        authenticated_client, request_body_update, model_id
    )
    response_update_json = response_update.json()
    updated_model_id = response_update_json["next_id"]

    response_history = send_get_model_history_request(
        authenticated_client, {}, model_id
    )
    history_json = response_history.json()

    assert response_history.status_code == 200
    assert len(history_json) > 0

    latest_version = history_json[0]
    assert latest_version["_id"] == updated_model_id
    assert latest_version["name"] == "test_get_model_history"
    assert latest_version["owner_id"] == model_data["owner_id"]
    assert latest_version["deleted"] is False

    assert len(latest_version["properties"]) == len(updated_properties)
    for j, payload in enumerate(latest_version["properties"]):
        assert payload["payload"]["_id"] == updated_properties[j]["_id"]
        assert payload["payload"]["name"] == updated_properties[j]["name"]
        assert (
            payload["payload"]["properties"][0]["name"]
            == updated_properties[j]["properties"][0]["name"]
        )
        assert (
            payload["payload"]["properties"][0]["is_required"]
            == updated_properties[j]["properties"][0]["is_required"]
        )

    old_version = history_json[1]
    assert old_version["_id"] == model_id
    assert old_version["name"] == "test_get_model_history"
    assert old_version["owner_id"] == model_data["owner_id"]
    assert old_version["deleted"] is False

    assert len(old_version["properties"]) == len(model_data["properties"])
    for j, payload in enumerate(old_version["properties"]):
        assert payload["payload"]["_id"] == model_data["properties"][j]["id"]
        assert payload["is_required"] == model_data["properties"][j]["is_required"]


def test_get_model_history_with_deleted_model(authenticated_client):
    properties = build_properties(
        authenticated_client,
        "props_for_test_get_model_history_with_deleted_model",
        "props_for_test_get_model_history_with_deleted_model",
    )
    model_data = create_and_send_model_request(
        authenticated_client, "test_get_model_history_with_deleted_model", properties
    )
    model_id = model_data["_id"]

    response_delete = send_delete_model_request(authenticated_client, {}, model_id)
    response_delete_json = response_delete.json()

    response_history = send_get_model_history_request(
        authenticated_client, {}, model_id
    )
    response_history_json = response_history.json()

    assert response_history.status_code == 200
    assert response_delete_json["deleted"] == response_history_json[0]["deleted"]
    assert response_delete_json["_id"] == response_history_json[0]["_id"]
    for i, property in enumerate(response_delete_json["properties"]):
        assert (
            property["id"]
            == response_history_json[0]["properties"][i]["payload"]["_id"]
        )
