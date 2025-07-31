import pytest
import time
import fastapi

from properties.templates_properties import add_property_template
from properties.sends_properties import send_add_property_request

from models.templates_models import add_model_template
from models.sends_models import send_add_model_request

from objects.templates_objects import add_object_template
from objects.sends_objects import (
    send_add_object_request,
    send_get_count_objects_request,
)


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


def test_get_count_objects(authenticated_client, setup_data):
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

    response_get_count_objects = send_get_count_objects_request(
        authenticated_client, {}, 1, 10
    )

    response_get_count_objects_json = response_get_count_objects.json()

    assert response_get_count_objects.status_code == 200
    assert response_get_count_objects_json["total"] == 52
