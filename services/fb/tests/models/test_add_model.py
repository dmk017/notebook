from models.templates_models import add_model_template
from models.sends_models import send_add_model_request
from models.utils_models import (
    build_properties,
    build_properties_for_model,
    create_and_send_model_request,
)
from properties.test_add_property import add_property


def assert_model(original, verifiable):
    assert len(verifiable["properties"]) == len(original["properties"])
    for expected_property, actual_property in zip(
        original["properties"], verifiable["properties"]
    ):
        assert actual_property["id"] == expected_property["id"]
        assert actual_property["is_required"] == expected_property["is_required"]


def test_add_model(authenticated_client):
    properties = build_properties(
        authenticated_client, f"props_for_test_add_model", f"props_for_test_add_model"
    )
    response = create_and_send_model_request(
        authenticated_client, "test_model", properties
    )

    assert_model(
        add_model_template("test_model", build_properties_for_model(properties)),
        response,
    )


def test_add_model_with_empty_properties(authenticated_client):
    request_body = add_model_template(
        name="test_add_model_with_empty_properties", properties=[]
    )
    response = send_add_model_request(authenticated_client, request_body)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["name"] == "test_add_model_with_empty_properties"
    assert response_json["properties"] == []


def test_add_model_with_invalid_properties(authenticated_client):
    response_property = add_property(
        authenticated_client,
        "props_for_test_add_model_with_invalid_properties",
        "props_for_test_add_model_with_invalid_properties",
    )
    response_property_json = response_property.json()
    id_property = response_property_json["_id"]

    properties = [{"id": id_property, "is_required": "not_a_boolean"}]
    request_body = add_model_template(
        name="test_add_model_with_invalid_properties", properties=properties
    )
    response = send_add_model_request(authenticated_client, request_body)
    response_json = response.json()

    assert response.status_code == 422
    assert (
        response_json["detail"][0]["msg"]
        == "Input should be a valid boolean, unable to interpret input"
    )


def test_add_model_with_duplicated_properties(authenticated_client):
    response_property = add_property(
        authenticated_client,
        "props_for_test_add_model_with_duplicated_properties",
        "props_for_test_add_model_with_duplicated_properties",
    )
    response_property_json = response_property.json()
    id_property = response_property_json["_id"]

    duplicate_properties = [
        {"id": id_property, "is_required": False},
        {"id": id_property, "is_required": False},
    ]
    request_body = add_model_template(
        name="test_add_model_with_invalid_properties", properties=duplicate_properties
    )
    response = send_add_model_request(authenticated_client, request_body)

    assert response.status_code == 200


def test_add_model_with_missing_required_properties(authenticated_client):
    response_property = add_property(
        authenticated_client,
        "props_for_test_add_model_with_missing_required_properties",
        "props_for_test_add_model_with_missing_required_properties",
    )
    response_property_json = response_property.json()
    id_property = response_property_json["_id"]

    properties = [{"id": id_property}]
    request_body = add_model_template(
        name="test_add_model_with_missing_required_properties", properties=properties
    )
    response = send_add_model_request(authenticated_client, request_body)
    response_json = response.json()

    assert response.status_code == 422
    assert response_json["detail"][0]["msg"] == "Field required"
