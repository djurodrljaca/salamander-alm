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

from database.connection import Connection
from database.table import Table
from typing import Optional


class UserAuthenticationParameterTable(Table):
    """
    Base class for "user_authentication_parameter" table

    Table's columns:

    - user_id:  int, references user.id, unique
    - name:     str
    - value:    str
    """

    def __init__(self):
        """
        Constructor
        """
        Table.__init__(self)

    def create(self, connection: Connection) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        raise NotImplementedError()

    def read_authentication_parameters(self,
                                       connection: Connection,
                                       user_id: int) -> Optional[dict]:
        """
        Reads authentication parameters for the specified user

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    Authentication parameters

        Returned dictionary contains all of the users authentication parameters (names depend on
        the authentication type).

        Example of a returned dictionary:

        {"password_hash": "4252397432974634",
         "domain_name": "EXAMPLE"}
        """
        raise NotImplementedError()

    def insert_rows(self,
                    connection: Connection,
                    user_id: int,
                    authentication_parameters: dict) -> bool:
        """
        Inserts new rows in the table

        :param connection:                  Database connection
        :param user_id:                     ID of the user
        :param authentication_parameters:   User's authentication parameters

        :return:    Success or failure
        """
        raise NotImplementedError()

    def delete_rows(self, connection: Connection, user_id: int) -> None:
        """
        Deletes authentication parameters for the specified user

        :param connection:  Database connection
        :param user_id:     ID of the user authentication
        """
        raise NotImplementedError()
