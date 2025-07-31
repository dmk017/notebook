from src.config import get_settings
from src.objects.data.constants import MULTIPLE_DELIMETER, MULTIPLE_SYMBOL, REQUIRED_SYMBOL
from src.objects.objects_service_schema import (PropertyPayloadValues,
                                                       TPayloadValues)

SERVICE_SYMBOLS = [REQUIRED_SYMBOL, MULTIPLE_SYMBOL]


def row_to_property_parser(row: dict) -> list[PropertyPayloadValues]:
    result_property_payload_map = {}
    for (key, value) in row.items():
        (property_name, property_data_name, *values) = map(
            lambda header_value: header_value.translate(str.maketrans('', '', ''.join(SERVICE_SYMBOLS))),
            key.split(get_settings().file_templates_header_delimeter)
        )
        item = TPayloadValues(
            name=property_data_name,
            values=value.split(MULTIPLE_DELIMETER)
        )
        if result_property_payload_map.get(property_name) is None:
            result_property_payload_map[property_name] = [item]
        else:
            result_property_payload_map[property_name].append(item)
    return [PropertyPayloadValues(
        property_name=k,
        data=v
    ) for (k, v) in result_property_payload_map.items()]
