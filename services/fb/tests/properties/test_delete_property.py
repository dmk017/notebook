from properties.test_add_property import assert_property, add_property
from properties.sends_properties import send_delete_property_request


def test_delete_property(authenticated_client):
    property_name = f"test_delete_property"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    response_property_json = response_property.json()
    id_property = response_property.json()["_id"]

    response = send_delete_property_request(authenticated_client, {}, [], id_property)
    response_json = response.json()

    assert response.status_code == 200
    assert_property(response_property_json, response_json)
    assert response_json["deleted"]
