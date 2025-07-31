import pytest
import fastapi
import time

from properties.templates_properties import add_property_template
from properties.sends_properties import send_add_property_request

from models.templates_models import add_model_template
from models.sends_models import send_add_model_request

from objects.templates_objects import add_object_template
from objects.sends_objects import send_add_object_request


PRIMITIVE_TYPES = ["STR", "NUMBER", "DATE", "BOOL", "FILE"]


@pytest.mark.parametrize(
    "primitive_type, valid_value, invalid_value",
    [
        ("STR", "Тестовая строка", 1234),
        ("NUMBER", "12345", "тест"),
        ("DATE", "2023-10-01", "неверная_дата"),
        ("BOOL", "True", "123"),
    ],
)
def test_add_object_with_various_property_types(
    authenticated_client, setup_data, primitive_type, valid_value, invalid_value
):
    prop_name = f"Тестовое свойство {primitive_type}"
    property_template = add_property_template(
        name=prop_name,
        prop_name=prop_name,
        primitive_type=primitive_type,
        help_text=f"Пример: {valid_value}",
        is_required=True,
        is_multiple=False,
        validation=".*" if primitive_type == "STR" else "",
    )
    response_property = send_add_property_request(
        authenticated_client, property_template, []
    )

    assert response_property.status_code == 200

    property_id = response_property.json().get("_id")

    assert property_id is not None

    model_request = add_model_template(
        name=f"TestModel_{primitive_type}",
        properties=[{"id": property_id, "is_required": True}],
    )
    response_add_model = send_add_model_request(authenticated_client, model_request)

    assert response_add_model.status_code == 200

    model_id = response_add_model.json().get("_id")

    assert model_id is not None

    properties_for_object = [
        {
            "property_name": prop_name,
            "data": [{"name": prop_name, "values": [valid_value]}],
        }
    ]

    add_object_request_body = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    response_add_object = send_add_object_request(
        authenticated_client, add_object_request_body, []
    )

    assert response_add_object.status_code == 200

    response_add_object_json = response_add_object.json()

    assert response_add_object_json.get("model_id") == model_id
    assert valid_value in str(
        response_add_object_json["payload"][0]["data"][0]["values"][0]
    )

    properties_for_object_invalid = [
        {
            "property_name": prop_name,
            "data": [{"name": prop_name, "values": [invalid_value]}],
        }
    ]

    if primitive_type == "STR":
        with pytest.raises(
            TypeError, match="expected string or bytes-like"
        ) as exc_info:
            add_object_request_body_invalid = add_object_template(
                model_id=model_id, properties=properties_for_object_invalid
            )
            response_add_object_invalid = send_add_object_request(
                authenticated_client, add_object_request_body_invalid, []
            )

        assert "expected string or bytes-like" in str(exc_info.value)
    elif (
        primitive_type == "NUMBER"
        or primitive_type == "DATE"
        or primitive_type == "BOOL"
    ):
        with pytest.raises(
            fastapi.exceptions.ResponseValidationError, match="validation"
        ) as exc_info:
            add_object_request_body_invalid = add_object_template(
                model_id=model_id, properties=properties_for_object_invalid
            )
            response_add_object_invalid = send_add_object_request(
                authenticated_client, add_object_request_body_invalid, []
            )

            assert (
                "Input should be a valid dictionary or object to extract fields"
                in response_add_object_invalid.json()["msg"]
            )
    else:
        add_object_request_body_invalid = add_object_template(
            model_id=model_id, properties=properties_for_object_invalid
        )
        response_add_object_invalid = send_add_object_request(
            authenticated_client, add_object_request_body_invalid, []
        )

        assert response_add_object_invalid.status_code == 400


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


def test_add_object(authenticated_client, setup_data):
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

    assert response_add_object.status_code == 200
    assert "_id" in response_add_object_json
    assert response_add_object_json["_id"] is not None
    assert response_add_object_json["model_id"] == model_id

    assert len(response_add_object_json["payload"]) == 2
    assert (
        response_add_object_json["payload"][0]["data"][0]["values"][0] == "Иванов Иван"
    )
    assert (
        response_add_object_json["payload"][1]["data"][0]["values"][0] == "+78005553535"
    )


def test_add_object_with_multiple_values(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [
                {
                    "name": f"ФИО_{unique_suffix}",
                    "values": ["Иванов Иван", "Петров Петр"],
                }
            ],
        },
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [
                {
                    "name": f"Номер телефона_{unique_suffix}",
                    "values": ["+78005553535", "+79005553535"],
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


def test_add_object_with_invalid_values(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": ["12345"]}],
        }
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )

    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)


def test_add_object_with_empty_values(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"ФИО_{unique_suffix}",
            "data": [{"name": f"ФИО_{unique_suffix}", "values": []}],
        }
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )
    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)


def test_add_object_with_wrong_data_format(authenticated_client, setup_data):
    unique_suffix, model_id = setup_data

    properties_for_object = [
        {
            "property_name": f"Номер телефона_{unique_suffix}",
            "data": [
                {"name": f"Номер телефона_{unique_suffix}", "values": ["не_номер"]}
            ],
        }
    ]

    object_template = add_object_template(
        model_id=model_id, properties=properties_for_object
    )

    with pytest.raises(fastapi.exceptions.ResponseValidationError) as exc_info:
        send_add_object_request(authenticated_client, object_template)

    assert "OBJECT_ADD_REQUEST_MALFORMED" in str(exc_info.value)
