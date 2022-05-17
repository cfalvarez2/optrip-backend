from datetime import datetime
from pytz import utc, timezone


def datetime_current(timezone_location: str = ""):
    """
    :return: datetime in timezone
    """
    tz = utc
    if timezone_location:
        tz = timezone(timezone_location)
    return datetime.now(tz=tz).replace(microsecond=0)


def convert_datetime_to_iso_8601(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
