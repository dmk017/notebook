import os
import pandas as pd

from models.sends_models import send_get_example_file_model_request
from models.utils_models import build_properties, create_and_send_model_request


def test_get_example_file_model(authenticated_client):
    properties = build_properties(
        authenticated_client,
        "props_for_test_get_example_file_model",
        "props_for_test_get_example_file_model",
    )
    model_data = create_and_send_model_request(
        authenticated_client, "test_get_example_file_model", properties
    )
    model_id = model_data["_id"]

    response = send_get_example_file_model_request(authenticated_client, {}, model_id)

    assert response.status_code == 200

    content_type = response.headers.get("Content-Type")
    assert content_type == "application/vnd.ms-excel"

    current_directory = os.getcwd()
    filepath = os.path.join(current_directory, "tests", "models", "example_file.xlsx")

    with open(filepath, "wb") as f:
        f.write(response.content)

    assert os.path.exists(filepath), "Файл не был сохранен."

    df = pd.read_excel(filepath, engine="openpyxl")
    data_dict = df.to_dict(orient="records")

    assert len(data_dict) > 0

    expected_headers = [f"props_for_test_get_example_file_model_{i}" for i in range(5)]

    for header in expected_headers:
        assert header in data_dict[0], f"Header '{header}' not found in the first row."

    expected_values_row_0 = [
        f"props_for_test_get_example_file_model_{i}" for i in range(5)
    ]

    for i, header in enumerate(expected_headers):
        assert (
            data_dict[0][header] == expected_values_row_0[i]
        ), f"Value for '{header}' does not match expected."

    expected_values_row_1 = "Тип значаний: строка (например: мама мыла раму)"

    for i, header in enumerate(expected_headers):
        assert (
            data_dict[1][header] == expected_values_row_1
        ), f"Value for '{header}' in the second row does not match expected."
