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
from typing import List, Optional


class UserTable(object):
    """
    Base class for "user" table
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def __del__(self):
        """
        Destructor
        """
        pass

    def create(self, connection: Connection) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        raise NotImplementedError()

    def read_all_users(self, connection: Connection) -> List[int]:
        """
        Reads IDs of all users in the database

        :param connection:  Database connection

        :return:    List of user IDs
        """
        raise NotImplementedError()

    def insert_row(self, connection: Connection) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection

        :return:    ID of the newly created row
        """
        raise NotImplementedError()
