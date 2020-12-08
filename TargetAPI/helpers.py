from datetime import datetime

def string_to_datetime(date_string: str, template: str = "%Y-%m-%dT%H:%M:%S.000Z") -> datetime:
    """
    Convert a datetime string to a datetime.datetime object
    :param date_string: datetime string to convert
    :param template: (Optional) datetime template to use when parsing string
    :return: datetime.datetime object
    :rtype: datetime.datetime
    """
    return datetime.strptime(date_string, template)