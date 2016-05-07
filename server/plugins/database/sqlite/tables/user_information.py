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
from database.tables.user_information import UserInformationTable
import sqlite3
from typing import Any, Optional


class UserInformationTableSqlite(UserInformationTable):
    """
    Implementation of "user_information" table for SQLite database
    """

    def __init__(self):
        """
        Constructor
        """
        UserInformationTable.__init__(self)

    def __del__(self):
        """
        Destructor
        """
        UserInformationTable.__del__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE user_information (\n"
            "    id           INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                         NOT NULL,\n"
            "    user_id      INTEGER REFERENCES user (id) \n"
            "                         NOT NULL,\n"
            "    user_name    TEXT    NOT NULL\n"
            "                         CHECK (length(user_name) > 0),\n"
            "    display_name TEXT    NOT NULL\n"
            "                         CHECK (length(display_name) > 0),\n"
            "    email        TEXT,\n"
            "    active       BOOLEAN NOT NULL\n"
            "                         CHECK ( (active = 0) OR\n"
            "                                 (active = 1) ),\n"
            "    revision_id  INTEGER REFERENCES revision (id) \n"
            "                         NOT NULL\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX user_information_ix_user_name ON user_information (\n"
            "    user_name\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX user_information_ix_display_name ON user_information (\n"
            "    display_name\n"
            ")")

    def read_information(self,
                         connection: ConnectionSqlite,
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
        # Read the users that match the search attribute
        query = (
            "SELECT user_id,\n"
            "       user_name,\n"
            "       display_name,\n"
            "       email,\n"
            "       active,\n"
            "       revision_id\n"
            "FROM (\n"
            "    SELECT UI1.user_id,\n"
            "           UI1.user_name,\n"
            "           UI1.display_name,\n"
            "           UI1.email,\n"
            "           UI1.active,\n"
            "           UI1.revision_id\n"
            "    FROM user_information AS UI1\n"
            "    WHERE (UI1.revision_id = (\n"
            "                SELECT MAX(UI2.revision_id)\n"
            "                FROM user_information AS UI2\n"
            "                WHERE ((UI2.user_id = UI1.user_id) AND\n"
            "                       (UI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ")\n"
        )

        if only_active_users:
            query += ("WHERE (({0} = :attribute_value) AND\n"
                      "       (active = 1))")
        else:
            query += "WHERE ({0} = :attribute_value)"

        cursor = connection.native_connection.execute(query.format(attribute_name),
                                                      {"attribute_value": attribute_value,
                                                       "max_revision_id": max_revision_id})

        # Process result
        users = list()

        for row in cursor.fetchall():
            if row is not None:
                user = {"user_id": row["user_id"],
                        "user_name": row["user_name"],
                        "display_name": row["display_name"],
                        "email": row["email"],
                        "active": bool(row["active"]),
                        "revision_id": row["revision_id"]}
                users.append(user)

        return users

    def insert_row(self,
                   connection: ConnectionSqlite,
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
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO user_information\n"
                "   (id, user_id, user_name, display_name, email, active, revision_id)\n"
                "VALUES (NULL, :user_id, :user_name, :display_name, :email, :active, :revision_id)",
                {"user_id": user_id,
                 "user_name": user_name,
                 "display_name": display_name,
                 "email": email,
                 "active": active,
                 "revision_id": revision_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
