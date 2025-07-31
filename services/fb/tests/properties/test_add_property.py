import pytest
import httpx
import itertools

from properties.data_properties import PRIMITIVE_TYPES
from properties.sends_properties import (
    send_add_property_request,
    send_delete_property_request,
)
from properties.templates_properties import add_property_template


def add_property(authenticated_client, name, prop_name):
    request_body = add_property_template(
        name=name,
        prop_name=prop_name,
        primitive_type="STR",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )
    return send_add_property_request(authenticated_client, request_body, [])


def assert_property(original, verifiable):
    assert verifiable["name"] == original["name"]
    assert verifiable["owner_id"] == "42ca4873-1229-4379-91c3-bb9704f57cab"
    assert len(verifiable["properties"]) == len(original["properties"])
    for expected_property, actual_property in zip(
        original["properties"], verifiable["properties"]
    ):
        assert actual_property["name"] == expected_property["name"]
        assert actual_property["primitive_type"] == expected_property["primitive_type"]
        assert actual_property["help_text"] == expected_property["help_text"]
        assert actual_property["is_required"] == expected_property["is_required"]
        assert actual_property["is_multiple"] == expected_property["is_multiple"]
        assert actual_property["validation"] == expected_property["validation"]


def test_add_full_property(authenticated_client):
    COUNT = 1

    combinations = [
        {
            "prop_name": ["", "test-prop"],
            "primitive_type": PRIMITIVE_TYPES,
            "help_text": ["", "help_text"],
            "is_required": [False, True],
            "is_multiple": [False, True],
            "validation": ["", "^.{2,}$"],
        }
    ]

    keys = combinations[0].keys()
    values = [combinations[0][key] for key in keys]

    for combination in itertools.islice(itertools.product(*values), 160, None):
        request_body = add_property_template(
            name=f"test_add_full_property_{COUNT}",
            prop_name=combination[0],
            primitive_type=combination[1],
            help_text=combination[2],
            is_required=combination[3],
            is_multiple=combination[4],
            validation=combination[5],
        )

        response = send_add_property_request(authenticated_client, request_body, [])
        response_json = response.json()

        assert (
            response.status_code == 200
        ), f"Bad request for primitive type: {combination[1]}"
        assert (
            "_id" in response_json
        ), f"Bad response for primitive type: {combination[1]}"
        assert (
            "properties" in response_json
        ), f"Bad response for primitive type: {combination[1]}"
        assert_property(
            request_body, response_json
        ), f"Bad response for primitive type: {combination[1]}"
        id_property = response_json["_id"]

        response_delete = send_delete_property_request(
            authenticated_client, {}, [], id_property
        )
        response_delete_json = response_delete.json()

        assert response_delete.status_code == 200
        assert_property(response_json, response_delete_json)
        assert response_delete_json["deleted"]

        COUNT += 1


def test_add_property_with_missing_name(authenticated_client):
    request_body = add_property_template(
        prop_name="test_add_property_with_missing_name",
        primitive_type="STR",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )

    response = send_add_property_request(authenticated_client, request_body, [])
    response_json = response.json()

    assert response.status_code == 200
    assert_property(request_body, response_json)
    id_property = response_json["_id"]

    response_delete = send_delete_property_request(
        authenticated_client, {}, [], id_property
    )
    response_delete_json = response_delete.json()

    assert response_delete.status_code == 200
    assert_property(response_json, response_delete_json)
    assert response_delete_json["deleted"]


def test_add_property_with_invalid_type(authenticated_client):
    request_body = add_property_template(
        name=f"test_add_property_with_invalid_type",
        prop_name="test",
        primitive_type="INVALID_TYPE",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )

    response = send_add_property_request(authenticated_client, request_body, [])

    assert response.status_code == 422


def test_add_property_with_long_prop_name(authenticated_client):
    request_body = add_property_template(
        name=f"test_add_property_with_long_prop_name",
        prop_name="a" * 1000000,
        primitive_type="STR",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )

    with pytest.raises(httpx.InvalidURL) as exc_info:
        send_add_property_request(authenticated_client, request_body, [])

    assert "URL component 'query' too long" in str(exc_info.value)


def test_add_property_with_special_characters_in_name(authenticated_client):
    request_body = add_property_template(
        name="test_add_property_with_special_characters_in_name",
        prop_name="test@prop#name$",
        primitive_type="STR",
        help_text="help_test",
        is_required=False,
        is_multiple=False,
        validation="^.{2,}$",
    )
    response = send_add_property_request(authenticated_client, request_body, [])

    assert response.status_code == 200
    assert "_id" in response.json()

    id_property = response.json()["_id"]
    response_delete = send_delete_property_request(
        authenticated_client, {}, [], id_property
    )

    assert response_delete.status_code == 200


def test_add_property_with_missing_fields(authenticated_client):
    property_name = f"test_add_property_with_missing_fields"

    request_body = {
        "name": property_name,
        "prop_name": property_name,
    }
    response = send_add_property_request(authenticated_client, request_body, [])

    assert "Field required" in response.json()["detail"][0]["msg"]
