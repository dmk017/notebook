import os
import zipfile
import pandas as pd
import pytest

from properties.templates_properties import add_property_template
from properties.sends_properties import send_add_property_request

from models.templates_models import add_model_template
from models.sends_models import send_add_model_request

from objects.templates_objects import (
    add_object_template,
    unloading_objects_template,
    approve_objects_template,
)
from objects.sends_objects import (
    send_add_object_request,
    send_unloading_objects,
    send_approve_objects_request,
)


@pytest.fixture
def properties(authenticated_client):
    properties_info = [
        {
            "name": "FIO",
            "prop_name": "FIO",
            "primitive_type": "STR",
            "help_text": "Пример: Иванов Иван Иванович",
            "is_required": True,
            "is_multiple": False,
            "validation": "^[А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23}$",
        },
        {
            "name": "Phone number",
            "prop_name": "Phone number",
            "primitive_type": "STR",
            "help_text": "Пример: +78005553535",
            "is_required": False,
            "is_multiple": False,
            "validation": "((8|\+7)[\-\.]?)?(\(?\d{3}\)?[\-\.]?)?[\d\-\.]{7,10}",
        },
        {
            "name": "VK Page",
            "prop_name": "VK Page",
            "primitive_type": "STR",
            "help_text": "Пример: https://vk.com/username",
            "is_required": False,
            "is_multiple": False,
            "validation": "^(https?\:\/\/)?(www\.)?vk\.com\/(\w|\d)+?\/?$",
        },
    ]

    responses = []
    for prop in properties_info:
        response = send_add_property_request(
            authenticated_client, add_property_template(**prop), []
        )
        assert response.status_code == 200
        responses.append(response.json())

    return responses


@pytest.fixture
def models(authenticated_client, properties):
    model_info = [
        (properties[0]["_id"], True, "MyModel1"),
        (properties[1]["_id"], False, "MyModel2"),
        (properties[2]["_id"], False, "MyModel3"),
    ]

    responses = []
    for prop_id, is_required, model_name in model_info:
        response = send_add_model_request(
            authenticated_client,
            add_model_template(
                name=model_name,
                properties=[{"id": prop_id, "is_required": is_required}],
            ),
        )
        assert response.status_code == 200
        responses.append(response.json())

    return responses


@pytest.fixture
def objects(authenticated_client, models):
    object_info = [
        (models[0]["_id"], "Иванов Иван", "FIO"),
        (models[1]["_id"], "+78912341212", "Phone number"),
        (models[2]["_id"], "https://vk.com/username", "VK Page"),
    ]

    object_ids = []
    for model_id, value, property_name in object_info:
        properties_for_object = [
            {
                "property_name": property_name,
                "data": [{"name": property_name, "values": [value]}],
            },
        ]
        response = send_add_object_request(
            authenticated_client,
            add_object_template(model_id=model_id, properties=properties_for_object),
        )
        assert response.status_code == 200
        object_ids.append(response.json()["_id"])

    return object_ids


def test_unloading_objects_with_approved_filters(
    authenticated_client, properties, models, objects
):
    approve_objects_request = approve_objects_template(objects[:2])
    response_approve_objects = send_approve_objects_request(
        authenticated_client, approve_objects_request, []
    )
    assert response_approve_objects.status_code == 200
    assert response_approve_objects.text == "2"

    filters = [
        {
            "type": "group",
            "group": "AND",
            "key": "STATUS_FILTER",
            "conditions": [
                {
                    "type": "isolated",
                    "property": "status",
                    "operator": "eq",
                    "value": "approved",
                }
            ],
        }
    ]

    unloading_objects_request = unloading_objects_template("", filters)
    response_unloading_objects = send_unloading_objects(
        authenticated_client, unloading_objects_request, []
    )

    assert response_unloading_objects.status_code == 200

    file_name = (
        response_unloading_objects.headers["content-disposition"]
        .split("filename=")[1]
        .strip('"')
    )

    current_directory = os.getcwd()
    xls_files_directory = os.path.join(
        current_directory, "tests", "objects", "xls_files"
    )

    os.makedirs(xls_files_directory, exist_ok=True)

    file_path = os.path.join(xls_files_directory, file_name)

    with open(file_path, "wb") as f:
        f.write(response_unloading_objects.content)

    assert os.path.exists(file_path), "Файл не был сохранен."

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_file_list = zip_ref.namelist()

        data_frames = []
        for excel_file in zip_file_list:
            excel_file_path = zip_ref.extract(excel_file, path=xls_files_directory)

            df = pd.read_excel(excel_file_path)

            assert not df.empty, "The Excel file is empty."
            assert len(df.columns) > 0, "The Excel file has no columns."

            df = df.astype(str)
            data_frames.append(df)

    combined_df = pd.concat(data_frames, ignore_index=True)

    assert (
        combined_df.iloc[0].tolist()[0] == "78912341212"
    ), "Values in the first row do not match."

    assert (
        combined_df.iloc[1].tolist()[1] == "Иванов Иван"
    ), "Values in the second row do not match."
