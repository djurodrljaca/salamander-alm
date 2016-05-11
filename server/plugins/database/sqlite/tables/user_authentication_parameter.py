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
from database.tables.user_authentication_parameter import UserAuthenticationParameterTable
import sqlite3
from typing import Optional


class UserAuthenticationParameterTableSqlite(UserAuthenticationParameterTable):
    """
    Implementation of "user_authentication_parameter" table for SQLite database

    Table's columns:

    - user_id:  int, references user.id, unique
    - name:     str
    - value:    str
    """

    def __init__(self):
        """
        Constructor
        """
        UserAuthenticationParameterTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE user_authentication_parameter (\n"
            "    user_id     INTEGER REFERENCES user (id)\n"
            "                        NOT NULL\n"
            "                        UNIQUE,\n"
            "    name        TEXT    NOT NULL,\n"
            "    value       TEXT    NOT NULL\n"
            ")")

    def read_authentication_parameters(self,
                                       connection: ConnectionSqlite,
                                       user_id: int) -> Optional[dict]:
        """
        Reads authentication parameters for the specified user

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    Authentication parameters

        Returned dictionary contains all of the users authentication parameters (names depend on
        the authentication type).

        Example of a returned dictionary:

        {"password_hash": "4252397432974634",
         "domain_name": "EXAMPLE"}
        """
        cursor = connection.native_connection.execute(
            "SELECT name,\n"
            "       value\n"
            "FROM user_authentication_parameter\n"
            "WHERE (user_id = :user_id)",
            {"user_id": user_id})

        # Process result
        authentication_parameters = None
        rows = cursor.fetchall()

        if len(rows) > 0:
            authentication_parameters = dict()

            for row in rows:
                authentication_parameters[row["name"]] = row["value"]

        return authentication_parameters

    def insert_rows(self,
                    connection: ConnectionSqlite,
                    user_id: int,
                    authentication_parameters: dict) -> bool:
        """
        Inserts new rows in the table

        :param connection:                  Database connection
        :param user_id:                     ID of the user
        :param authentication_parameters:   User's authentication parameters

        :return:    Success or failure
        """
        value_array = list()

        for key in authentication_parameters.keys():
            value_item = {"user_id": user_id,
                          "name": key,
                          "value": authentication_parameters[key]}
            value_array.append(value_item)

        try:
            cursor = connection.native_connection.executemany(
                "INSERT INTO user_authentication_parameter"
                "   (user_id,\n"
                "    name,\n"
                "    value)\n"
                "VALUES (:user_id,\n"
                "        :name,\n"
                "        :value)",
                value_array)

            if cursor.rowcount == len(value_array):
                success = True
        except sqlite3.IntegrityError:
            # Error occurred
            success = False

        return success

    def delete_rows(self, connection: ConnectionSqlite, user_id: int) -> None:
        """
        Deletes authentication parameters for the specified user

        :param connection:  Database connection
        :param user_id:     ID of the user authentication
        """
        connection.native_connection.execute(
            "DELETE FROM user_authentication_parameter\n"
            "WHERE (user_id = :user_id)",
            {"user_id": user_id})
