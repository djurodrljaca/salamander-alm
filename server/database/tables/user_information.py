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
from typing import Any, Optional


class UserInformationTable(object):
    """
    Base class for "user_information" table
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

    def read_information(self,
                         connection: Connection,
                         attribute_name: str,
                         attribute_value: Any,
                         only_active_users: bool,
                         max_revision_id: int) -> Optional[dict]:
        """
        Reads user information for the specified user, state (active/inactive) and max revision

        :param connection:          Database connection
        :param attribute_name:      Search attribute name
        :param attribute_value:     Search attribute value
        :param only_active_users:   Only search for active users
        :param max_revision_id:     Maximum revision ID for the search

        :return: User information of all users that match the search attribute

        Only the following search attributes are supported:
        - user_id
        - user_name
        - display_name
        - email
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   user_id: int,
                   user_name: str,
                   display_name: str,
                   email: str,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:      Database connection
        :param user_id:         ID of the user
        :param user_name:       User name
        :param display_name:    User's name in format appropriate for displaying in the GUI
        :param email:           Email address of the user
        :param active:          State of the user (active or inactive)
        :param revision_id:     Revision ID

        :return: ID of the newly created row
        """
        raise NotImplementedError()
