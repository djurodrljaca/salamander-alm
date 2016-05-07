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
from database.tables.user_authentication import UserAuthenticationTable
import sqlite3
from typing import Optional


class UserAuthenticationTableSqlite(UserAuthenticationTable):
    """
    Implementation of "user_authentication" table for SQLite database
    """

    def __init__(self):
        """
        Constructor
        """
        UserAuthenticationTable.__init__(self)

    def __del__(self):
        """
        Destructor
        """
        UserAuthenticationTable.__del__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE user_authentication (\n"
            "    id            INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                          NOT NULL,\n"
            "    user_id       INTEGER REFERENCES user (id) \n"
            "                          NOT NULL,\n"
            "    type          TEXT    NOT NULL\n"
            "                          CHECK (length(type) > 0),\n"
            "    revision_id   INTEGER REFERENCES revision (id) \n"
            "                          NOT NULL\n"
            ")")

    def read_authentication(self,
                            connection: ConnectionSqlite,
                            user_id: int,
                            max_revision_id: int) -> Optional[dict]:
        """
        Reads authentication information for the specified user and max revision

        :param connection:      Database connection
        :param user_id:         ID of the user
        :param max_revision_id: Maximum revision ID for the search

        :return:    Authentication information
        """
        cursor = connection.native_connection.execute(
            "SELECT id, type\n"
            "FROM user_authentication\n"
            "WHERE ((user_id = :user_id) AND\n"
            "       (revision_id = (\n"
            "           SELECT MAX(revision_id)\n"
            "           FROM user_authentication\n"
            "           WHERE ((user_id = :user_id) AND\n"
            "                  (revision_id <= :max_revision_id))\n"
            "        )))",
            {"user_id": user_id,
             "max_revision_id": max_revision_id})

        # Process result
        authentication = None
        row = cursor.fetchone()

        if row is not None:
            authentication = dict(row)

        return authentication

    def insert_row(self,
                   connection: ConnectionSqlite,
                   user_id: int,
                   type: str,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param user_id:     ID of the user
        :param type:        User's authentication type
        :param revision_id: Revision ID

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO user_authentication\n"
                "   (id, user_id, type, revision_id)\n"
                "VALUES (NULL, :user_id, :type, :revision_id)",
                {"user_id": user_id,
                 "type": type,
                 "revision_id": revision_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
