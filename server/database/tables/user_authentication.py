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


class UserAuthenticationTable(Table):
    """
    Base class for "user_authentication" table

    Table's columns:

    - user_id:              int, references user.id, unique
    - authentication_type:  str
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

    def read_authentication(self, connection: Connection, user_id: int) -> Optional[dict]:
        """
        Reads authentication information for the specified user

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    Authentication information

        Returned dictionary contains items:

        - id
        - user_id
        - authentication_type
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   user_id: int,
                   authentication_type: str) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:          Database connection
        :param user_id:             ID of the user
        :param authentication_type: User's authentication type

        :return:    ID of the newly created row
        """
        raise NotImplementedError()

    def update_row(self,
                   connection: Connection,
                   user_authentication_id: int,
                   authentication_type: str) -> bool:
        """
        Updates a row in the table

        :param connection:          Database connection
        :param user_id:             ID of the user
        :param authentication_type: User's new authentication type

        :return:    Success or failure
        """
        raise NotImplementedError()
