from properties.test_add_property import assert_property, add_property
from properties.sends_properties import (
    send_get_property_by_id_request,
    send_delete_property_request,
)


def test_get_property_by_id(authenticated_client):
    property_name = f"test_get_property_by_id"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    response = send_get_property_by_id_request(
        authenticated_client, {}, [], id_property
    )
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property.json(), response_json)


def test_get_property_by_id_with_deleted_property(authenticated_client):
    property_name = "test_get_property_by_id_with_deleted_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    send_delete_property_request(authenticated_client, {}, [], id_property)

    response = send_get_property_by_id_request(
        authenticated_client, {}, [], id_property
    )

    assert response.status_code == 200
    assert_property(response_property.json(), response.json())
