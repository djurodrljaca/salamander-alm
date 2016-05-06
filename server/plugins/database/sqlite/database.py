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

from database.database import Database, Tables
import os
from plugins.database.sqlite.connection import ConnectionSqlite
from plugins.database.sqlite.tables.revision import RevisionTableSqlite
from plugins.database.sqlite.tables.user import UserTableSqlite
from plugins.database.sqlite.tables.user_authentication import UserAuthenticationTableSqlite
from plugins.database.sqlite.tables.user_authentication_basic \
    import UserAuthenticationBasicTableSqlite
from plugins.database.sqlite.tables.user_information import UserInformationTableSqlite
import sqlite3
from typing import Any, Optional


class DatabaseSqlite(Database):
    """
    SQLite database object
    """

    def __init__(self, database_file_path: str):
        """
        Constructor

        :param database_file_path:  Database file path
        """
        tables = Tables()

        tables.revision = RevisionTableSqlite()

        tables.user = UserTableSqlite()
        tables.user_authentication = UserAuthenticationTableSqlite()
        tables.user_authentication_basic = UserAuthenticationBasicTableSqlite()
        tables.user_information = UserInformationTableSqlite()

        Database.__init__(self, tables)

        self.__database_file_path = database_file_path

        self.__application_id = 0x53414c4d  # HEX for "SALM"
        self.__encoding = "\"UTF-8\""
        self.__user_version = 1             # Version of the database file

    def __del__(self):
        """
        Destructor
        """
        Database.__del__(self)

    def create_connection(self) -> Optional[ConnectionSqlite]:
        """
        Creates a new database connection

        :return:    Database connection instance
        """
        connection = sqlite3.connect(self.__database_file_path)
        connection.row_factory = sqlite3.Row

        # Set non-persistent PRAGMA values
        self.__update_pragma(connection, "foreign_keys", 1)

        return ConnectionSqlite(connection)

    def _create_database(self) -> bool:
        """
        Creates an empty database if needed

        :return:    Success or failure
        """
        if os.path.exists(self.__database_file_path):
            # Error, database already exists!
            return False

        connection = sqlite3.connect(self.__database_file_path)

        # Set persistent PRAGMA values
        self.__update_pragma(connection, "application_id", self.__application_id)
        self.__update_pragma(connection, "encoding", self.__encoding)

        # TODO: set to "0" here and write to correct version when database is initialized?
        self.__update_pragma(connection, "user_version", self.__user_version)

        connection.commit()
        connection.close()
        return True

    def __read_pragma(self, connection: sqlite3.Connection, name: str) -> Any:
        """
        Reads PRAGMA value

        :param connection:  Database connection
        :param name:        Pragma's name
        """
        cursor = connection.execute("PRAGMA {0}".format(name))

        value = None
        row = cursor.fetchone()

        if row is not None:
            value = row[0]

        return value

    def __update_pragma(self, connection: sqlite3.Connection, name: str, value: Any) -> None:
        """
        Updates PRAGMA value

        :param connection:  Database connection
        :param name:        Pragma's name
        :param value:       Pragma's value
        """
        connection.execute("PRAGMA {0} = {1}".format(name, str(value)))
