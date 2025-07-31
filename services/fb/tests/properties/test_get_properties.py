import pytest

from properties.test_add_property import assert_property, add_property
from properties.templates_properties import get_properties_template
from properties.sends_properties import (
    send_get_properties_request,
    send_delete_property_request,
)


def get_properties(authenticated_client, name, is_deleted=False, page=1, limit=10):
    request_body = get_properties_template(name=name, is_deleted=is_deleted)
    response = send_get_properties_request(
        authenticated_client, request_body, [], page, limit
    )
    return response


def test_get_properties_with_deleted_property(authenticated_client):
    property_name = f"test_get_properties_with_deleted_property"
    response = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response.json()["_id"]

    response_before = get_properties(
        authenticated_client, name=property_name, is_deleted=False
    )
    response_before_json = response_before.json()

    send_delete_property_request(authenticated_client, {}, [], id_property)

    response_after = get_properties(
        authenticated_client, name=property_name, is_deleted=False
    )
    response_after_json = response_after.json()

    assert response.status_code == 200
    assert len(response_after_json) == len(response_before_json)
    for i in range(len(response_after_json)):
        assert_property(response_after_json[i], response_before_json[i])


def test_get_properties_with_deleted_flag(authenticated_client):
    property_name = f"test_get_properties_with_deleted_flag"
    response_property = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )
    id_property = response_property.json()["_id"]

    send_delete_property_request(authenticated_client, {}, [], id_property)

    response = get_properties(authenticated_client, name=property_name, is_deleted=True)

    assert response.status_code == 200
    assert response.json() != []


def test_get_properties_with_nonexistent_name(authenticated_client):
    property_name = f"test_get_properties_with_nonexistent_name"
    response = add_property(
        authenticated_client, name=property_name, prop_name=property_name
    )

    response = get_properties(
        authenticated_client, name="nonexistent-name", is_deleted=False
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json != []


def test_get_properties_with_empty_name(authenticated_client):
    response = get_properties(authenticated_client, name="", is_deleted=False)
    response_json = response.json()

    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert len(response_json) > 0


def test_get_properties_with_invalid_limit_1(authenticated_client):
    response = get_properties(
        authenticated_client, name="test", is_deleted=False, limit=-1
    )

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_properties_with_invalid_limit_2(authenticated_client):
    response = get_properties(
        authenticated_client, name="test", is_deleted=False, limit=-2
    )

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_properties_with_deleted_properties_only(authenticated_client):
    COUNT = 3
    property_names = [
        f"test_get_properties_with_deleted_properties_only_{i}" for i in range(COUNT)
    ]
    responses = []

    for name in property_names:
        response = add_property(authenticated_client, name=name, prop_name=name)
        responses.append(response.json())

    for response in responses:
        send_delete_property_request(authenticated_client, {}, [], response["_id"])

    response = get_properties(
        authenticated_client,
        name="test_get_properties_with_deleted_properties_only",
        is_deleted=True,
    )
    response_json = response.json()

    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert len(response_json) > 0
