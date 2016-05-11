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
import enum
from typing import Any, List, Optional


class UserSelection(enum.Enum):
    """
    User selection
    """
    Active = 1,
    Inactive = 2,
    All = 3


class UserTable(Table):
    """
    Base class for "user" table

    Table's columns:

    - id:           int
    - user_name:    str
    - display_name: str
    - email:        Optional[str]
    - active:       bool
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

    def read_all_ids(self, connection: Connection, user_selection: UserSelection) -> List[int]:
        """
        Reads IDs of all users in the database

        :param connection:      Database connection
        :param user_selection:  Search for active, inactive or all users

        :return:    List of user IDs
        """
        raise NotImplementedError()

    def read_users_by_attribute(self,
                                connection: Connection,
                                attribute_name: str,
                                attribute_value: Any,
                                user_selection: UserSelection) -> List[dict]:
        """
        Reads information of all users that match the specified search attribute

        :param connection:      Database connection
        :param attribute_name:  Search attribute name
        :param attribute_value: Search attribute value
        :param user_selection:  Search for active, inactive or all users

        :return:    User information of all users that match the search attribute

        Only the following search attributes are supported:

        - id
        - user_name
        - display_name
        - email

        Each dictionary in the returned list contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   user_name: str,
                   display_name: str,
                   email: str,
                   active: bool) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:      Database connection
        :param user_name:       User name
        :param display_name:    User's name in format appropriate for displaying in the GUI
        :param email:           Email address of the user
        :param active:          State of the user (active or inactive)

        :return:    ID of the newly created row
        """
        raise NotImplementedError()

    def update_row(self,
                   connection: Connection,
                   user_id: int,
                   user_name: str,
                   display_name: str,
                   email: str,
                   active: bool) -> bool:
        """
        Updates a row in the table

        :param connection:      Database connection
        :param user_id:         ID of the user
        :param user_name:       User's new user name
        :param display_name:    User's new display name
        :param email:           User's new email address
        :param active:          User's new state (active or inactive)

        :return:    Success or failure
        """
        raise NotImplementedError()
