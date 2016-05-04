"""
Salamander ALM
Copyright (c) 2016  Djuro Drljaca

This Python module is free software; you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This Python module is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library. If
not, see <http://www.gnu.org/licenses/>.
"""

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
