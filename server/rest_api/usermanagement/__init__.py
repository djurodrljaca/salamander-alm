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

from rest_api.application import api
from rest_api.usermanagement import login, logout, user


def _create_url(relative_url: str) -> str:
    """
    Creates a full URL from a relative URL

    :param relative_url:    Relative part of the URL

    :return:    Full URL

    Example:
    - Relative URL: "login"
    - Returned URL: "/api/usermanagement/login"
    """
    return "/api/usermanagement/" + relative_url


if api is not None:
    # Add all resources from this package
    api.add_resource(login.Login, _create_url("login"))
    api.add_resource(logout.Logout, _create_url("logout"))
    api.add_resource(user.User, _create_url("user"))
