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

from authentication.authentication import AuthenticationInterface
from database.connection import Connection
from database.tables.revision import RevisionTable
from database.tables.user import UserTable
from database.tables.user_authentication import UserAuthenticationTable
from database.tables.user_authentication_parameter import UserAuthenticationParameterTable
from database.tables.user_information import UserInformationTable
import datetime
from typing import Optional


class Tables(object):
    """
    Class that holds all of the tables in the database
    """

    def __init__(self):
        """
        Constructor
        """
        self.revision = RevisionTable()
        self.user = UserTable()
        self.user_authentication = UserAuthenticationTable()
        self.user_authentication_parameter = UserAuthenticationParameterTable()
        self.user_information = UserInformationTable()


class Database(object):
    """
    Base class for a database object
    """

    def __init__(self, tables: Tables):
        """
        Constructor

        :param tables:  Concrete implementations of database tables
        """
        self.__tables = tables

    def __del__(self):
        """
        Destructor
        """
        pass

    def tables(self):
        """
        Property for accessing the database tables

        :return:    Database tables
        """
        return self.__tables

    def validate(self) -> bool:
        """
        Validates the database

        :return:    Success or failure

        During validation the tables are checked
        """
        raise NotImplementedError()

    def create_new_database(self) -> bool:
        """
        Creates a new database

        :return:    Success or failure

        NOTE:   This should only be called during initial configuration of the application after it
                is installed (when the database is still empty)!
        """
        # First create the database
        success = self._create_database()

        # Then initialize it
        if success:
            connection = self.create_connection()

            try:
                connection.begin_transaction()

                if success:
                    self.__create_all_tables(connection)

                if success:
                    success = self.__create_default_system_users(connection)

                if success:
                    success = self.__create_default_system_groups(connection)

                if success:
                    connection.commit_transaction()
                else:
                    connection.rollback_transaction()
            except:
                connection.rollback_transaction()
                raise

        return success

    def create_connection(self) -> Optional[Connection]:
        """
        Creates a new database connection

        :return:    Database connection instance
        """
        raise NotImplementedError()

    def _create_database(self) -> bool:
        """
        Creates an empty database if needed

        :return:    Success or failure
        """
        raise NotImplementedError()

    def __create_all_tables(self, connection: Connection):
        """
        Creates all the database tables

        :param connection:  Database connection
        """
        # Create tables
        self.__tables.revision.create(connection)
        self.__tables.user.create(connection)
        self.__tables.user_authentication.create(connection)
        self.__tables.user_authentication_parameter.create(connection)
        self.__tables.user_information.create(connection)

    def __create_default_system_users(self, connection: Connection) -> bool:
        """
        Creates the default system users

        :param connection:  Database connection

        :return:    Success or failure
        """
        # Since the database doesn't contain any users we must first create just the ID of the
        # Administrator user, then create the first revision that is referencing the Administrator
        # and then finally write all of the other user information and authentication.
        success = True
        user_id = self.__tables.user.insert_row(connection)

        if user_id is None:
            success = False

        revision_id = None

        if success:
            revision_id = self.__tables.revision.insert_row(connection,
                                                            datetime.datetime.utcnow(),
                                                            user_id)

            if revision_id is None:
                success = False

        if success:
            user_information_id = self.__tables.user_information.insert_row(connection,
                                                                            user_id,
                                                                            "administrator",
                                                                            "Administrator",
                                                                            "",
                                                                            True,
                                                                            revision_id)

            if user_information_id is None:
                success = False

        user_authentication_id = None

        if success:
            user_authentication_id = self.__tables.user_authentication.insert_row(connection,
                                                                                  user_id,
                                                                                  "basic")

        if user_authentication_id is None:
            success = False

        if success:
            authentication_parameters = \
                AuthenticationInterface.generate_reference_authentication_parameters(
                    "basic",
                    {"password": "administrator"})

            user_authentication_basic_id = self.__tables.user_authentication_parameter.insert_rows(
                connection,
                user_authentication_id,
                authentication_parameters)

            if user_authentication_basic_id is None:
                success = False

        return success

    def __create_default_system_groups(self, connection: Connection) -> bool:
        """
        Creates the default system user groups

        :param connection:  Database connection

        :return:    Success or failure
        """
        # TODO: implement
        return True


class DatabaseInterface(object):
    """
    Interface to the database (singleton)

    Dependencies:
    - AuthenticationInterface
    """

    __database_object = None   # Database instance

    def __init__(self):
        """
        Constructor is disabled!
        """
        raise RuntimeError()

    @staticmethod
    def load_database_plugin(database_object: Database) -> None:
        """
        Load a Database object

        :param database_object: Database object
        """
        if not isinstance(database_object, Database):
            raise AttributeError()

        DatabaseInterface.__database_object = database_object

    @staticmethod
    def tables() -> Tables:
        """
        Get database tables

        :return:    Database tables
        """
        return DatabaseInterface.__database_object.tables()

    @staticmethod
    def validate() -> bool:
        """
        Validates the database

        :return:    Success or failure

        During validation the tables are checked
        """
        return DatabaseInterface.__database_object.validate()

    @staticmethod
    def create_new_database() -> bool:
        """
        Creates a new database

        :return:    Success or failure

        NOTE:   This should only be called during initial configuration of the application after it
                is installed (when the database is still empty)!
        """
        return DatabaseInterface.__database_object.create_new_database()

    @staticmethod
    def create_connection() -> Optional[Connection]:
        """
        Creates a new database connection

        :return:    Database connection instance
        """
        return DatabaseInterface.__database_object.create_connection()
