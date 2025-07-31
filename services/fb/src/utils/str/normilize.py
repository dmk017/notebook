from transliterate import translit


def normilize(value: str) -> str:
    value = translit(value, 'ru', reversed=True)  # do eng letter
    value = value.replace(' ', '_')
    return value
