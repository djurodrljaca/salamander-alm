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
from typing import Optional


class UserAuthenticationBasicTable(object):
    """
    Base class for "user_authentication_basic" table
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

    def read_password_hash(self,
                           connection: Connection,
                           user_authentication_id: int,
                           max_revision_id: int) -> str:
        """
        Reads authentication information for the specified user and max revision

        :param connection:              Database connection
        :param user_authentication_id:  ID of the user authentication
        :param max_revision_id:         Maximum revision ID for the search

        :return: Password hash
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   user_authentication_id: int,
                   password_hash: str,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  D           atabase connection
        :param user_authentication_id:  ID of the user authentication
        :param password_hash:           User's password hash
        :param revision_id:             Revision ID

        :return: ID of the newly created row
        """
        raise NotImplementedError()

