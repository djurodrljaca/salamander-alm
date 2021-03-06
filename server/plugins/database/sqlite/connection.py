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
import sqlite3


class ConnectionSqlite(Connection):
    """
    SQLite database connection
    """
    def __init__(self, native_connection: sqlite3.Connection):
        """
        Constructor

        :param native_connection: Native connection object
        """
        Connection.__init__(self)

        # Disable automatic transactions and save the connection object
        native_connection.isolation_level = None
        self.__native_connection = native_connection
        self.__in_transaction = False

    def __del__(self):
        """
        Destructor
        """
        Connection.__del__(self)

    @property
    def native_connection(self) -> sqlite3.Connection:
        """
        Returns the native connection

        :return:
        """
        return self.__native_connection

    @property
    def in_transaction(self) -> bool:
        """
        Checks if a transaction is active on the connection

        :return:    Transaction is active or not
        """
        return self.__in_transaction

    def begin_transaction(self) -> bool:
        """
        Begins a transaction

        :return:    Success or failure
        """
        if self.__in_transaction:
            return False

        self.native_connection.execute("BEGIN")
        self.__in_transaction = True
        return True

    def commit_transaction(self) -> bool:
        """
        Commits the currently active transaction

        :return:    Success or failure
        """
        if not self.__in_transaction:
            return False

        self.native_connection.execute("COMMIT")
        self.__in_transaction = False
        return True

    def rollback_transaction(self) -> bool:
        """
        Rolls back the currently active transaction

        :return:    Success or failure
        """
        if not self.__in_transaction:
            return False

        self.native_connection.execute("ROLLBACK")
        self.__in_transaction = False
        return True
