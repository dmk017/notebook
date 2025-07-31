

decoder = {
    "true": True,
    "false": False
}


def bool_decoder(value) -> bool:
    if isinstance(value, bool):
        return value
    result = decoder.get(value.lower())
    if result is None:
        raise f"Value '{value}' dont conversion to bool"
    return result
