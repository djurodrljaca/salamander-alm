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

from flask import request
from flask_restful import Resource, abort
from usermanagement.user_management import UserManagementInterface, Connection
from typing import Optional


class RestrictedResource(Resource):
    """
    Extension of the Resource class that contains parsing for session token in the request
    """

    def __init__(self):
        """
        Constructor
        """
        Resource.__init__(self)

    @staticmethod
    def _read_session_token() -> str:
        """
        Reads the session token from the request

        :return:    Session token
        """
        # Extract arguments from the request
        if "SALM-Session-Token" in request.headers:
            return request.headers["SALM-Session-Token"]
        else:
            abort(400, message="Access denied, please log in and try again")


    @staticmethod
    def _read_session_user(connection: Connection, token: str) -> Optional[dict]:
        """
        Reads the user information that belongs to the session

        :param connection:  Database connection
        :param token:       Session token

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active

        Note:   User information is returned only if the user exists and if it is active
        """
        # Read session token
        session_token = UserManagementInterface.read_session_token(connection, token)

        if session_token is None:
            # Error, invalid token
            return None

        # Check if session's user is active
        user = UserManagementInterface.read_user_by_id(connection, session_token["user_id"])

        if user is None:
            # Error, user was not found
            return None

        if not user["active"]:
            # Error, user is not active
            return None

        return user
