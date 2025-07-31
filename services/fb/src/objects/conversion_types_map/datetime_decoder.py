import datetime
from typing import Union

from dateutil.parser import parse


def dateime_decoder(value: Union[str, datetime.datetime]) -> datetime.datetime:
    if isinstance(value, datetime.date):
        return value
    return parse(value)
