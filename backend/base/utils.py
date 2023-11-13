from backend.core.settings import DATETIME_FORMAT


def date_time_format(date_time):
    """Return datetime format"""
    result = None
    if date_time is not None:
        result = date_time.strftime(DATETIME_FORMAT)
    return result
