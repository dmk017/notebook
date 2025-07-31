from properties.test_add_property import assert_property, add_property
from properties.sends_properties import (
    send_delete_property_request,
    send_get_property_history,
    send_update_property_request,
)
from properties.templates_properties import add_property_template


def test_get_history_of_property_with_no_history(authenticated_client):
    property_name = f"test_get_history_of_property_with_no_history"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    response = send_get_property_history(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property.json(), response_json[0])


def test_get_history_of_deleted_property(authenticated_client):
    property_name = f"test_get_history_of_deleted_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    send_delete_property_request(authenticated_client, {}, [], id_property)

    response = send_get_property_history(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property.json(), response_json[0])


def test_get_history_of_property_with_multiple_changes(authenticated_client):
    property_name = f"test_get_history_of_property_with_multiple_changes"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    for i in range(3):
        request_body = add_property_template(
            name=f"test_get_history_of_property_with_multiple_changes",
            prop_name=f"test_get_history_of_property_with_multiple_changes_{i}",
            primitive_type="STR",
            help_text="123",
            is_required=False,
            is_multiple=False,
            validation="^.{2,}$",
        )
        send_update_property_request(
            authenticated_client, request_body, [], id_property
        )

    response = send_get_property_history(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 4
