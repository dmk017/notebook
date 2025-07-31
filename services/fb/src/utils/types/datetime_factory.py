import datetime
import pytz
from tzlocal import get_localzone

def dt_factory() -> datetime:
  tz = pytz.timezone('Europe/Moscow')
  dt =  datetime.datetime.now(datetime.timezone.utc)
  return dt.astimezone(tz=tz).isoformat()
