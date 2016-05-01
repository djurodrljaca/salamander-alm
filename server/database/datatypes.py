from datetime import datetime


def datetime_to_string(dt: datetime) -> str:
    """
    Convert a datetime object to a string

    :param dt: Datetime object

    :return: String representation of a datetime object

    Note: Make sure that the datetime object is in UTC!
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


def datetime_from_string(dt_string: str) -> datetime:
    """
    Convert a string to a datetime object

    :param dt_string: String representing a datetime object

    :return: String representation of a datetime object
    """
    return datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%f")
