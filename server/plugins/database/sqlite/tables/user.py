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

from plugins.database.sqlite.connection import ConnectionSqlite
from database.tables.user import UserTable, UserSelection
from typing import Any, List, Optional
import sqlite3


class UserTableSqlite(UserTable):
    """
    Implementation of "user" table for SQLite database

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
        UserTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE user (\n"
            "    id           INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                         NOT NULL,\n"
            "    user_name    TEXT    NOT NULL\n"
            "                         CHECK (length(user_name) > 0),\n"
            "    display_name TEXT    NOT NULL\n"
            "                         CHECK (length(display_name) > 0),\n"
            "    email        TEXT,\n"
            "    active       BOOLEAN NOT NULL\n"
            "                         CHECK ( (active = 0) OR\n"
            "                                 (active = 1) )\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX user_ix_user_name ON user (\n"
            "    user_name\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX user_ix_display_name ON user (\n"
            "    display_name\n"
            ")")

    def read_all_ids(self,
                     connection: ConnectionSqlite,
                     user_selection: UserSelection) -> List[int]:
        """
        Reads IDs of all users in the database

        :param connection:      Database connection
        :param user_selection:  Search for active, inactive or all users

        :return:    List of user IDs
        """
        query = (
            "SELECT id\n"
            "FROM user\n"
        )

        if user_selection == UserSelection.Active:
            query += "WHERE (active = 1)"
        elif user_selection == UserSelection.Inactive:
            query += "WHERE (active = 0)"
        else:
            # Nothing needed for selecting all users
            pass

        cursor = connection.native_connection.execute(query)

        users = list()

        for row in cursor.fetchall():
            users.append(row[0])

        return users

    def read_users_by_attribute(self,
                                connection: ConnectionSqlite,
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
        if attribute_name not in ["id", "user_name", "display_name", "email"]:
            raise AttributeError("Unsupported attribute name")

        # Read the users that match the search attribute
        query = (
            "SELECT id,\n"
            "       user_name,\n"
            "       display_name,\n"
            "       email,\n"
            "       active\n"
            "FROM user\n"
        )

        if user_selection == UserSelection.Active:
            query += ("WHERE (({0} = :attribute_value) AND\n"
                      "       (active = 1))")
        elif user_selection == UserSelection.Inactive:
            query += ("WHERE (({0} = :attribute_value) AND\n"
                      "       (active = 0))")
        else:
            query += "WHERE ({0} = :attribute_value)"

        cursor = connection.native_connection.execute(query.format(attribute_name),
                                                      {"attribute_value": attribute_value})

        # Process result
        users = list()

        for row in cursor.fetchall():
            if row is not None:
                user = {"id": row["id"],
                        "user_name": row["user_name"],
                        "display_name": row["display_name"],
                        "email": row["email"],
                        "active": bool(row["active"])}
                users.append(user)

        return users

    def insert_row(self,
                   connection: ConnectionSqlite,
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
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO user\n"
                "   (id,\n"
                "    user_name,\n"
                "    display_name,\n"
                "    email,\n"
                "    active)\n"
                "VALUES (NULL,\n"
                "        :user_name,\n"
                "        :display_name,\n"
                "        :email,\n"
                "        :active)",
                {"user_name": user_name,
                 "display_name": display_name,
                 "email": email,
                 "active": active})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id

    def update_row(self,
                   connection: ConnectionSqlite,
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
        try:
            cursor = connection.native_connection.execute(
                "UPDATE user\n"
                "SET user_name = :user_name,\n"
                "    display_name = :display_name,\n"
                "    email = :email,\n"
                "    active = :active\n"
                "WHERE (id = :id)",
                {"id": user_id,
                 "user_name": user_name,
                 "display_name": display_name,
                 "email": email,
                 "active": active})

            if cursor.rowcount == 1:
                success = True
            else:
                success = False
        except sqlite3.IntegrityError:
            # Error occurred
            success = False

        return success
