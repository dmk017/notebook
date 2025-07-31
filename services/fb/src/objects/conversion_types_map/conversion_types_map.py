from src.objects.conversion_types_map.bool_decoder import bool_decoder
from src.objects.conversion_types_map.datetime_decoder import \
    dateime_decoder
from src.objects.conversion_types_map.number_decoder import \
    number_decoder
from src.objects.conversion_types_map.string_decoder import \
    string_decoder

conversion_types_map = {
    "STR": string_decoder,
    "NUMBER": number_decoder,
    "DATE": dateime_decoder,
    "BOOL": bool_decoder,
    "FILE": string_decoder
}


def conversion_type(type, value):
    if not value:
        return None
    try:
        return conversion_types_map.get(type)(value)
    except Exception:
        return None
