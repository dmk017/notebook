import pytest
import os

from models.templates_models import add_model_template
from models.sends_models import send_add_model_request

from properties.templates_properties import add_property_template
from properties.sends_properties import send_add_property_request

from objects.sends_objects import send_upload_file_request


def upload_file(client, filepath):
    with open(filepath, "rb") as file:
        file_content = file.read()
    response = send_upload_file_request(client, {"file": file_content})
    return response


@pytest.fixture
def setup_data(authenticated_client):
    fio_property = add_property_template(
        name="ФИО",
        prop_name="ФИО",
        primitive_type="STR",
        help_text="Пример: Иванов Иван Иванович",
        is_required=True,
        is_multiple=False,
        validation="^[А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23}$",
    )
    response_fio = send_add_property_request(authenticated_client, fio_property)
    response_fio_json = response_fio.json()

    model_template = add_model_template(
        name="Фамилии",
        properties=[{"id": response_fio_json["_id"], "is_required": True}],
    )
    model_response = send_add_model_request(authenticated_client, model_template)
    model_response_json = model_response.json()

    return model_response_json["_id"], response_fio_json["_id"]


def test_upload_file(authenticated_client, setup_data):
    _, _ = setup_data

    file_path = (
        "./tests/objects/upload_file.xls"
    )
    response_upload = upload_file(authenticated_client, file_path)
    response_upload_json = response_upload.json()

    assert response_upload.status_code == 200
    assert response_upload_json["success"] is True
    assert response_upload_json["message"] == "Success added 1 objects"
