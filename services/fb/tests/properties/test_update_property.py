from properties.test_add_property import assert_property, add_property
from properties.sends_properties import (
    send_update_property_request,
    send_get_property_by_id_request,
)
from properties.templates_properties import add_property_template


def test_update_property(authenticated_client):
    property_name = f"test_update_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    request_body = add_property_template(
        name=property_name,
        prop_name=property_name,
        primitive_type="STR",
        help_text="123",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )
    response_update = send_update_property_request(
        authenticated_client, request_body, [], id_property
    )
    next_id_property = response_update.json()["next_id"]

    response = send_get_property_by_id_request(
        authenticated_client, {}, [], next_id_property
    )
    response_json = response.json()

    assert response.status_code == 200
    assert_property(request_body, response_json)


def test_update_property_with_invalid_primitive_type(authenticated_client):
    property_name = f"test_update_property_with_invalid_primitive_type"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    request_body = add_property_template(
        name=property_name,
        prop_name=property_name,
        primitive_type="INVALID_TYPE",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )
    response_update = send_update_property_request(
        authenticated_client, request_body, [], id_property
    )

    assert response_update.status_code == 422


def test_update_property_with_missing_fields(authenticated_client):
    property_name = f"test_update_property_with_missing_fields"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    request_body = {
        "name": property_name,
        "prop_name": property_name,
    }
    response = send_update_property_request(
        authenticated_client, request_body, [], id_property
    )

    assert "Field required" in response.json()["detail"][0]["msg"]
