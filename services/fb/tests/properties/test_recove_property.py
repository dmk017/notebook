from properties.test_add_property import assert_property, add_property
from properties.sends_properties import (
    send_get_recove_property,
    send_delete_property_request,
)


def test_recove_property(authenticated_client):
    property_name = f"test_recove_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    response = send_get_recove_property(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property.json(), response_json)


def test_recove_deleted_property(authenticated_client):
    property_name = f"test_recove_deleted_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    response_delete = send_delete_property_request(
        authenticated_client, {}, [], id_property
    )
    assert response_delete.json()["deleted"]

    response = send_get_recove_property(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property.json(), response_json)
    assert response_json["deleted"] == False


def test_recove_property_after_multiple_deletions(authenticated_client):
    property_name = f"test_recove_property_after_multiple_deletions"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    response_first_delete = send_delete_property_request(
        authenticated_client, {}, [], id_property
    )
    assert response_first_delete.json()["deleted"]

    response = send_get_recove_property(authenticated_client, {}, [], id_property)

    assert response.status_code == 200
    assert_property(response_property.json(), response.json())
    assert response.json()["deleted"] == False

    response_second_delete = send_delete_property_request(
        authenticated_client, {}, [], id_property
    )
    assert response_second_delete.json()["deleted"]

    response = send_get_recove_property(authenticated_client, {}, [], id_property)

    assert response.status_code == 200
    assert_property(response_property.json(), response.json())
    assert response.json()["deleted"] == False
