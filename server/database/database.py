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
from database.tables.user import UserTable, UserSelection
from database.tables.user_authentication import UserAuthenticationTable
from database.tables.user_authentication_parameter import UserAuthenticationParameterTable
from database.tables.session_token import SessionTokenTable
from database.tables.revision import RevisionTable
from database.tables.project import ProjectTable
from database.tables.project_information import ProjectInformationTable
from database.tables.tracker import TrackerTable
from database.tables.tracker_field import TrackerFieldTable
from database.tables.tracker_field_information import TrackerFieldInformationTable
from database.tables.tracker_information import TrackerInformationTable
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
        self.user = UserTable()
        self.user_authentication = UserAuthenticationTable()
        self.user_authentication_parameter = UserAuthenticationParameterTable()

        self.session_token = SessionTokenTable()

        self.revision = RevisionTable()

        self.project = ProjectTable()
        self.project_information = ProjectInformationTable()

        self.tracker = TrackerTable()
        self.tracker_information = TrackerInformationTable()

        self.tracker_field = TrackerFieldTable()
        self.tracker_field_information = TrackerFieldInformationTable()


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
        Method for accessing the database tables

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
                    success = self.__create_first_revision(connection)

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
        self.__tables.user.create(connection)
        self.__tables.user_authentication.create(connection)
        self.__tables.user_authentication_parameter.create(connection)

        self.__tables.session_token.create(connection)

        self.__tables.revision.create(connection)

        self.__tables.project.create(connection)
        self.__tables.project_information.create(connection)

        self.__tables.tracker.create(connection)
        self.__tables.tracker_information.create(connection)

        self.__tables.tracker_field.create(connection)
        self.__tables.tracker_field_information.create(connection)

    def __create_default_system_users(self, connection: Connection) -> bool:
        """
        Creates the default system users

        :param connection:  Database connection

        :return:    Success or failure

        This method creates users:

        - "administrator"
        """
        # Since the database doesn't contain any users we must first create one (Administrator) and
        # then create the first revision that is referencing the Administrator
        # Create the user in the new revision
        user_id = DatabaseInterface.tables().user.insert_row(connection,
                                                             "administrator",
                                                             "Administrator",
                                                             "",
                                                             True)

        if user_id is None:
            return False

        # Add user authentication to the user
        user_authentication_id = self.__tables.user_authentication.insert_row(
            connection,
            user_id,
            "basic")

        if user_authentication_id is None:
            return False

        reference_authentication_parameters = \
            AuthenticationInterface.generate_reference_authentication_parameters(
                "basic",
                {"password": "administrator"})

        if reference_authentication_parameters is None:
            return False

        success = self.__tables.user_authentication_parameter.insert_rows(
            connection,
            user_id,
            reference_authentication_parameters)

        return success

    def __create_default_system_groups(self, connection: Connection) -> bool:
        """
        Creates the default system user groups

        :param connection:  Database connection

        :return:    Success or failure
        """
        # TODO: implement
        return True

    def __create_first_revision(self, connection: Connection) -> bool:
        """
        Creates the default system users

        :param connection:  Database connection

        :return:    Success or failure
        """
        # Get the administrator's user ID
        # Read the users that match the search attribute
        users = self.__tables.user.read_users_by_attribute(connection,
                                                           "user_name",
                                                           "administrator",
                                                           UserSelection.Active)

        user = None

        if users is not None:
            if len(users) == 1:
                user = users[0]

        if user is None:
            return False

        if user["id"] is None:
            return False

        revision_id = self.__tables.revision.insert_row(connection,
                                                        datetime.datetime.utcnow(),
                                                        user["id"])

        if revision_id is None:
            return False

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
