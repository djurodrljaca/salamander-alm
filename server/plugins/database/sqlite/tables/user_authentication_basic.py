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
from database.tables.user_authentication_basic import UserAuthenticationBasicTable
from typing import Optional


class UserAuthenticationBasicTableSqlite(UserAuthenticationBasicTable):
    """
    Implementation of "user_authentication_basic" table for SQLite database
    """

    def __init__(self):
        """
        Constructor
        """
        UserAuthenticationBasicTable.__init__(self)

    def __del__(self):
        """
        Destructor
        """
        UserAuthenticationBasicTable.__del__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE user_authentication_basic (\n"
            "    id                     INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                                   NOT NULL,\n"
            "    user_authentication_id INTEGER REFERENCES user (id) \n"
            "                                   NOT NULL,\n"
            "    password_hash          TEXT    NOT NULL,\n"
            "    revision_id            INTEGER REFERENCES revision (id) \n"
            "                                   NOT NULL\n"
            ")")

    def read_password_hash(self,
                           connection: ConnectionSqlite,
                           user_authentication_id: int,
                           max_revision_id: int) -> str:
        """
        Reads authentication information for the specified user and max revision

        :param connection:              Database connection
        :param user_authentication_id:  ID of the user authentication
        :param max_revision_id:         Maximum revision ID for the search

        :return: Password hash
        """
        cursor = connection.native_connection.execute(
            "SELECT password_hash\n"
            "FROM user_authentication_basic\n"
            "WHERE ((user_authentication_id = :user_authentication_id) AND\n"
            "       (revision_id = (\n"
            "           SELECT MAX(revision_id)"
            "           FROM user_authentication_basic\n"
            "           WHERE ((user_authentication_id = :user_authentication_id) AND\n"
            "                  (revision_id <= :max_revision_id))\n"
            "        )))",
            {"user_authentication_id": user_authentication_id,
             "max_revision_id": max_revision_id})

        # Process result
        password_hash = None
        row = cursor.fetchone()

        if row is not None:
            password_hash = row[0]

        return password_hash

    def insert_row(self,
                   connection: ConnectionSqlite,
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
        cursor = connection.native_connection.execute(
            "INSERT INTO user_authentication_basic"
            "   (id, user_authentication_id, password_hash, revision_id)\n"
            "VALUES (NULL, :user_authentication_id, :password_hash, :revision_id)",
            {"user_authentication_id": user_authentication_id,
             "password_hash": password_hash,
             "revision_id": revision_id})

        return cursor.lastrowid
