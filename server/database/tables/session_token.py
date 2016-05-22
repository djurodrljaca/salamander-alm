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
import datetime
from typing import List, Optional


class SessionTokenTable(Table):
    """
    Base class for "session_token" table

    Table's columns:

    - id:           int
    - user_id:      int, references user.id
    - created_on:   datetime
    - token:        str
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

    def read_token(self, connection: Connection, token: str) -> Optional[dict]:
        """
        Reads the session token from the database

        :param connection:  Database connection
        :param token:       Session token

        :return:    Session token

        Returned dictionary contains items:

        - id
        - user_id
        - created_on
        - token
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   user_id: int,
                   created_on: datetime.datetime,
                   token: str) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param user_id:     ID of the user
        :param created_on:  Timestamp when the token was created
        :param token:       Session token

        :return:    ID of the newly created row
        """
        raise NotImplementedError()

    def delete_all_rows(self, connection: Connection) -> None:
        """
        Removes all rows from the table

        :param connection:  Database connection
        """
        raise NotImplementedError()

    def delete_row_by_user_id(self, connection: Connection, user_id: int) -> None:
        """
        Removes all rows that belong to the specified used from the table

        :param connection:  Database connection
        :param user_id:     ID of the user
        """
        raise NotImplementedError()

    def delete_row_by_token(self, connection: Connection, token: str) -> None:
        """
        Removes the row that contains the specified token from the table

        :param connection:  Database connection
        :param token:       Session token
        """
        raise NotImplementedError()

    def delete_rows_before_timestamp(self, connection: Connection, timestamp: datetime) -> None:
        """
        Removes the rows that are older than the specified timestamp

        :param connection:  Database connection
        :param timestamp:   Timestamp
        """
        raise NotImplementedError()
