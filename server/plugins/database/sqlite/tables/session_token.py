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
from database.tables.session_token import SessionTokenTable
from database.datatypes import datetime_from_string, datetime_to_string
import datetime
import sqlite3
from typing import List, Optional


class SessionTokenTableSqlite(SessionTokenTable):
    """
    Implementation of "session_token" table for SQLite database

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
        SessionTokenTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE session_token (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    user_id     INTEGER REFERENCES user (id)\n"
            "                        NOT NULL,\n"
            "    created_on  TEXT    NOT NULL\n"
            "                        CHECK (length(created_on) >= 23),\n"
            "    token       TEXT    NOT NULL\n"
            "                        UNIQUE\n"
            "                        CHECK (length(token) = 32)\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX session_token_ix_user_id ON session_token (\n"
            "    user_id\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX session_token_ix_created_on ON session_token (\n"
            "    created_on\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX session_token_ix_token ON session_token (\n"
            "    token\n"
            ")")

    def read_token(self, connection: ConnectionSqlite, token: str) -> Optional[dict]:
        """
        Reads the session token from the database

        :param connection:  Database connection
        :param token:       Session token

        :return:    Session token object

        Returned dictionary contains items:

        - id
        - user_id
        - created_on
        - token
        """
        cursor = connection.native_connection.execute(
            "SELECT id,\n"
            "       user_id,\n"
            "       created_on,\n"
            "       token\n"
            "FROM session_token\n"
            "WHERE (token = :token)\n",
            {"token": token})

        # Process result
        session_token_object = None
        row = cursor.fetchone()

        if row is not None:
            session_token_object = dict(row)

        return session_token_object

    def insert_row(self,
                   connection: ConnectionSqlite,
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
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO session_token\n"
                "   (id,\n"
                "    user_id,\n"
                "    created_on,\n"
                "    token)\n"
                "VALUES (NULL,\n"
                "        :user_id,\n"
                "        :created_on,\n"
                "        :token)",
                {"user_id": user_id,
                 "created_on": datetime_to_string(created_on),
                 "token": token})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id

    def delete_all_rows(self, connection: ConnectionSqlite) -> bool:
        """
        Removes all rows from the table

        :param connection:  Database connection

        :return:    Success or failure
        """
        connection.native_connection.execute("DELETE FROM session_token")

    def delete_row_by_user_id(self, connection: ConnectionSqlite, user_id: int) -> bool:
        """
        Removes all rows that belong to the specified used from the table

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    Success or failure
        """
        connection.native_connection.execute(
            "DELETE FROM session_token\n"
            "WHERE (user_id = :user_id)",
            {"user_id": user_id})

    def delete_row_by_token(self, connection: ConnectionSqlite, token: str) -> bool:
        """
        Removes the row that contains the specified token from the table

        :param connection:  Database connection
        :param token:       Session token

        :return:    Success or failure
        """
        connection.native_connection.execute(
            "DELETE FROM session_token\n"
            "WHERE (token = :token)",
            {"token": token})

    def delete_rows_before_timestamp(self,
                                     connection: ConnectionSqlite,
                                     timestamp: datetime) -> bool:
        """
        Removes the rows that are older than the specified timestamp

        :param connection:  Database connection
        :param timestamp:   Timestamp

        :return:    Success or failure
        """
        connection.native_connection.execute(
            "DELETE FROM session_token\n"
            "WHERE (created_on < :timestamp)",
            {"timestamp": datetime_to_string(timestamp)})
