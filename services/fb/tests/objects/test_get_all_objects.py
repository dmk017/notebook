import pytest
import fastapi
import time

from models.templates_models import add_model_template
from models.sends_models import send_add_model_request

from properties.templates_properties import add_property_template
from properties.sends_properties import send_add_property_request

from objects.templates_objects import add_object_template
from objects.sends_objects import send_add_object_request, send_get_all_objects_request


@pytest.fixture
def setup_data(authenticated_client):
    unique_suffix = str(time.time())

    fio_property = add_property_template(
        name=f"ФИО_{unique_suffix}",
        prop_name=f"ФИО_{unique_suffix}",
        primitive_type="STR",
        help_text="Пример: Иванов Иван Иванович",
        is_required=True,
        is_multiple=False,
        validation="^[А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23}$",
    )

    phone_property = add_property_template(
        name=f"Номер телефона_{unique_suffix}",
        prop_name=f"Номер телефона_{unique_suffix}",
        primitive_type="STR",
        help_text="Пример: +78005553535",
        is_required=False,
        is_multiple=False,
        validation="((8|\+7)[\-\.]?)?(\(?\d{3}\)?[\-\.]?)?[\d\-\.]{7,10}",
    )

    response_fio = send_add_property_request(authenticated_client, fio_property)
    response_phone = send_add_property_request(authenticated_client, phone_property)

    response_fio_json = response_fio.json()
    response_phone_json = response_phone.json()

    properties = [
        {"id": response_fio_json["_id"], "is_required": True},
        {"id": response_phone_json["_id"], "is_required": False},
    ]

    model_template = add_model_template(
        name=f"MyModel_{unique_suffix}", properties=properties
    )
    model_response = send_add_model_request(authenticated_client, model_template)
    model_response_json = model_response.json()

    return unique_suffix, model_response_json["_id"]


def test_get_all_objects(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["Иванов Иван"]}],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [
                {"name": f"Номер телефона_{unique_suffix}", "values": ["+78005553535"]}
            ],
        },
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    response_add_object = send_add_object_request(authenticated_client, object_template)
    response_add_object_json = response_add_object.json()

    assert response_add_object_json["_id"] is not None

    response_get_objects = send_get_all_objects_request(
        authenticated_client, {}, page=1, limit=10
    )
    response_get_objects_json = response_get_objects.json()

    assert response_get_objects.status_code == 200
    assert "count" in response_get_objects_json
    assert response_get_objects_json["count"] > 0
    assert "data" in response_get_objects_json
    assert isinstance(response_get_objects_json["data"], list)

    added_object_id = response_add_object_json["_id"]
    found_object = next(
        (
            obj
            for obj in response_get_objects_json["data"]
            if obj["_id"] == added_object_id
        ),
        None,
    )

    assert (
        found_object is not None
    ), "The added object was not found in the retrieved objects"

    assert (
        found_object["model_id"] == model_id
    ), "Model ID in retrieved object does not match"

    added_payload = found_object["payload"]
    assert (
        len(added_payload) == 2
    ), "Payload length does not match the expected number of properties"
    assert (
        added_payload[0]["data"][0]["values"][0] == "Иванов Иван"
    ), "FIO value in retrieved object does not match"
    assert (
        added_payload[1]["data"][0]["values"][0] == "+78005553535"
    ), "Phone number value in retrieved object does not match"


def test_add_object_with_empty_values(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": []}],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [{"name": f"Номер телефона_{unique_suffix}", "values": []}],
        },
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)


def test_add_object_with_invalid_values(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["12345"]}],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [{"name": f"Номер телефона_{unique_suffix}", "values": ["abcde"]}],
        },
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)


def test_add_object_with_only_required_fields(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["Иванов Иван"]}],
        }
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    response_add_object = send_add_object_request(authenticated_client, object_template)
    response_add_object_json = response_add_object.json()

    assert response_add_object.status_code == 200
    assert response_add_object_json["_id"] is not None


def test_add_multiple_objects(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    objects_to_add = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["Иванов Иван"]}],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [
                {"name": f"Номер телефона_{unique_suffix}", "values": ["+78005553535"]}
            ],
        },
    ]

    for i in range(5):
        object_template = add_object_template(
            model_id=model_id, properties=objects_to_add
        )
        response_add_object = send_add_object_request(
            authenticated_client, object_template
        )
        response_add_object_json = response_add_object.json()

        assert response_add_object.status_code == 200
        assert response_add_object_json["_id"] is not None


def test_get_objects_with_pagination(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    for i in range(15):
        properties_for_object = [
            {
                "property_name": f"ФИО_{unique_suffix}",
                "data": [
                    {"name": f"ФИО_{unique_suffix}", "values": [f"Иванов Иван {i}"]}
                ],
            },
            {
                "property_name": f"Номер телефона_{unique_suffix}",
                "data": [
                    {
                        "name": f"Номер телефона_{unique_suffix}",
                        "values": [f"+7800555353_{i}"],
                    }
                ],
            },
        ]
        object_template = add_object_template(
            model_id=model_id, properties=properties_for_object
        )
        response_add_object = send_add_object_request(
            authenticated_client, object_template
        )
        assert (
            response_add_object.status_code == 200
        ), f"Failed to add object {i}: {response_add_object.json()}"

    response_get_objects_page_1 = send_get_all_objects_request(
        authenticated_client, {}, page=1, limit=10
    )
    response_get_objects_page_1_json = response_get_objects_page_1.json()

    assert response_get_objects_page_1.status_code == 200
    assert response_get_objects_page_1_json["count"] == 10
    assert len(response_get_objects_page_1_json["data"]) == 10

    response_get_objects_page_2 = send_get_all_objects_request(
        authenticated_client, {}, page=2, limit=10
    )
    response_get_objects_page_2_json = response_get_objects_page_2.json()

    assert response_get_objects_page_2.status_code == 200
    assert len(response_get_objects_page_2_json["data"]) == 10

    response_get_objects_page_3 = send_get_all_objects_request(
        authenticated_client, {}, page=3, limit=10
    )
    response_get_objects_page_3_json = response_get_objects_page_3.json()

    assert response_get_objects_page_3.status_code == 200
    assert len(response_get_objects_page_3_json["data"]) == 10


def test_add_object_with_valid_and_invalid_phone(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["Иванов Иван"]}],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [
                {
                    "name": f"Номер телефона_{unique_suffix}",
                    "values": ["+78005553535", "invalid_phone"],
                }
            ],
        },
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )

    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)
