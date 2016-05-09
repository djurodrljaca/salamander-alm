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

import datetime
from typing import Optional

from authentication.authentication import Authentication, AuthenticationMethod
from authentication.basic_authentication_method import AuthenticationMethodBasic
from database.connection import Connection
from database.database import Database


class UserManagement(object):
    """
    User management
    """

    def __init__(self, database_object: Database):
        """
        Constructor

        :param database_object: Database object
        """
        self.__database = database_object
        self.__authentication = Authentication()
        self.__authentication.add_authentication_method(AuthenticationMethodBasic())

    def __del__(self):
        """
        Destructor
        """
        pass

    def read_user_by_user_id(self, user_id: int) -> Optional[dict]:
        """
        Reads a user that matches the specified user ID

        :param user_id:             ID of the user

        :return:    User information object

        NOTE:   This method searches both active and inactive users
        """
        # First get the current revision
        connection = self.__database.create_connection()
        current_revision_id = self.__database.tables.revision.read_current_revision_id(connection)

        # Read a user that matches the specified user ID
        user = None

        if current_revision_id is not None:
            user = self.__read_user_by_user_id(connection, user_id, current_revision_id)

        return user

    def read_user_by_user_name(self, user_name: str) -> Optional[dict]:
        """
        Reads a user that matches the specified user ID

        :param user_name:           User's user name

        :return:    User information object

        NOTE:   This method only searches active users
        """
        # First get the current revision
        connection = self.__database.create_connection()
        current_revision_id = self.__database.tables.revision.read_current_revision_id(connection)

        # Read a user that matches the specified user ID
        user = None

        if current_revision_id is not None:
            user = self.__read_user_by_user_name(connection, user_name, current_revision_id)

        return user

    def read_users_by_user_name(self, user_name: str, only_active_users: bool) -> Optional[dict]:
        """
        Reads a user that matches the specified user ID

        :param user_name:           User's user name
        :param only_active_users:   Only search for active users

        :return:    User information object
        """
        # First get the current revision
        connection = self.__database.create_connection()
        current_revision_id = self.__database.tables.revision.read_current_revision_id(connection)

        # Read a user that matches the specified user ID
        users = None

        if current_revision_id is not None:
            users = self.__database.tables.user_information.read_information(connection,
                                                                             "user_name",
                                                                             user_name,
                                                                             only_active_users,
                                                                             current_revision_id)

        return users

    def read_users_by_display_name(self,
                                   display_name: str,
                                   only_active_users=True) -> Optional[dict]:
        """
        Reads a user that matches the specified user ID

        :param display_name:        User's display name
        :param only_active_users:   Only search for active users

        :return:    User information object
        """
        # First get the current revision
        connection = self.__database.create_connection()
        current_revision_id = self.__database.tables.revision.read_current_revision_id(connection)

        # Read a user that matches the specified user ID
        users = None

        if current_revision_id is not None:
            users = self.__database.tables.user_information.read_information(connection,
                                                                             "display_name",
                                                                             display_name,
                                                                             only_active_users,
                                                                             current_revision_id)

        return users

    def create_user(self,
                    requested_by_user: int,
                    user_name: str,
                    display_name: str,
                    email: str,
                    authentication_type: str,
                    authentication_parameters: dict) -> Optional[int]:
        """
        Create a new user

        :param requested_by_user:           ID of the user that requested creation of the new user
        :param user_name:                   User's user name
        :param display_name:                User's display name
        :param email:                       Email address of the user
        :param authentication_type:         User's authentication type
        :param authentication_parameters:   User's authentication parameters

        :return: User ID of the new user
        """
        user_id = None
        connection = self.__database.create_connection()

        try:
            success = connection.begin_transaction()

            # Start a new revision
            revision_id = None

            if success:
                revision_id = self.__database.tables.revision.insert_row(connection,
                                                                         datetime.datetime.utcnow(),
                                                                         requested_by_user)

                if revision_id is None:
                    success = False

            # Create the user
            if success:
                user_id = self.__create_user(connection,
                                             user_name,
                                             display_name,
                                             email,
                                             authentication_type,
                                             authentication_parameters,
                                             revision_id)

                if user_id is None:
                    success = False

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return user_id

    def update_user_information(self,
                                requested_by_user: int,
                                user_to_modify: int,
                                user_name: str,
                                display_name: str,
                                email: str,
                                active: bool) -> bool:
        """
        Update user's information

        :param requested_by_user:   ID of the user that requested modification of the user
        :param user_to_modify:      ID of the user that should be modified
        :param user_name:           User's user name
        :param display_name:        User's display name
        :param email:               User's email address
        :param email:               New email address of the user
        :param active:              New state of the user (active or inactive)

        :return:    Success or failure
        """
        connection = self.__database.create_connection()

        try:
            success = connection.begin_transaction()

            # Start a new revision
            revision_id = None

            if success:
                revision_id = self.__database.tables.revision.insert_row(connection,
                                                                         datetime.datetime.utcnow(),
                                                                         requested_by_user)

                if revision_id is None:
                    success = False

            # Check if there is already an existing user with the same user name
            if success:
                success = False
                user = self.__read_user_by_user_name(connection, user_name, revision_id)

                if user is None:
                    success = True
                elif user["user_id"] == user_to_modify:
                    success = True

            # Update user's information in the new revision
            if success:
                row_id = self.__database.tables.user_information.insert_row(connection,
                                                                            user_to_modify,
                                                                            user_name,
                                                                            display_name,
                                                                            email,
                                                                            active,
                                                                            revision_id)

                if row_id is None:
                    success = False

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success

    def add_authentication_method(self,
                                  authentication_method: AuthenticationMethod) -> bool:
        """
        Adds support for an authentication method

        :param authentication_method:   Authentication method

        :return:    Success or failure
        """
        return self.__authentication.add_authentication_method(authentication_method)

    def remove_all_authentication_methods(self) -> None:
        """
        Removes all authentication methods
        """
        self.__authentication.remove_all_authentication_methods()

    def read_user_authentication(self, user_id: int) -> Optional[dict]:
        """
        Reads a user's authentication

        :param user_id:             ID of the user

        :return:    User authentication object
        """
        connection = self.__database.create_connection()

        try:
            success = connection.begin_transaction()

            # Read the user's authentication
            user_authentication = None

            if success:
                user_authentication = self.__read_user_authentication(connection, user_id)

                if user_authentication is None:
                    success = False

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return user_authentication

    def authenticate_user(self, user_name: str, authentication_parameters: str) -> bool:
        """
        Authenticate user with basic authentication

        :param user_name:                   User's user name
        :param authentication_parameters:   User's authentication parameters

        :return:    Success or failure
        """
        connection = self.__database.create_connection()

        try:
            success = connection.begin_transaction()

            # Read the user that matches the specified user name
            if success:
                current_revision_id = self.__database.tables.revision.read_current_revision_id(
                    connection)

                if current_revision_id is None:
                    success = False

            user = None

            if success:
                user = self.__read_user_by_user_name(connection, user_name, current_revision_id)

                if user is None:
                    # Error, invalid user name
                    success = False
                elif not user["active"]:
                    # Error, user is not active
                    success = False

            # Read user's authentication information
            if success:
                user_authentication = self.__read_user_authentication(
                    connection,
                    user["user_id"])

                if user_authentication is None:
                    # Error, no authentication was found for that user
                    success = False

            # Authenticate user
            user_authenticated = False

            if success:
                user_authenticated = self.__authentication.authenticate(
                    user_authentication["authentication_type"],
                    authentication_parameters,
                    user_authentication["authentication_parameters"])

                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return user_authenticated

    def update_user_authentication(self,
                                   user_to_modify: int,
                                   authentication_type: str,
                                   authentication_parameters: dict) -> bool:
        """
        Update user's authentication

        :param user_to_modify:              ID of the user that should be modified
        :param authentication_type:         User's new authentication type
        :param authentication_parameters:   User's new authentication parameters

        :return: Success or failure
        """
        connection = self.__database.create_connection()

        try:
            success = connection.begin_transaction()

            # Update user's authentication
            user_authentication = None

            if success:
                # Read users current authentication information
                user_authentication = \
                    self.__database.tables.user_authentication.read_authentication(connection,
                                                                                   user_to_modify)

                if user_authentication is None:
                    # Error, no authentication was found for that user
                    success = False

            # Modify authentication type if needed
            if success and (authentication_type != user_authentication["authentication_type"]):
                success = self.__database.tables.user_authentication.update_authentication_type(
                    connection,
                    user_authentication["id"],
                    authentication_type)

            # Modify authentication parameters
            if success:
                success = False
                self.__database.tables.user_authentication_parameter.delete_rows(
                    connection,
                    user_authentication["id"])

                reference_authentication_parameters = \
                    self.__authentication.generate_reference_authentication_parameters(
                        authentication_type,
                        authentication_parameters)

                if reference_authentication_parameters is not None:
                    success = self.__database.tables.user_authentication_parameter.insert_rows(
                        connection,
                        user_authentication["id"],
                        reference_authentication_parameters)

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success

    def __read_user_by_user_id(self,
                               connection: Connection,
                               user_id: int,
                               max_revision_id: int) -> Optional[dict]:
        """
        Reads a user that matches the search parameters

        :param connection:          Database connection
        :param user_id:             ID of the user
        :param max_revision_id:     Maximum revision ID for the search

        :return:    User information object
        """
        # Read the users that match the search attribute
        users = self.__database.tables.user_information.read_information(connection,
                                                                         "user_id",
                                                                         user_id,
                                                                         False,
                                                                         max_revision_id)

        # Return a user only if exactly one was found
        user = None

        if users is not None:
            if len(users) == 1:
                user = users[0]

        return user

    def __read_user_by_user_name(self,
                                 connection: Connection,
                                 user_name: str,
                                 max_revision_id: int) -> Optional[dict]:
        """
        Reads a user that matches the search parameters

        :param connection:          Database connection
        :param user_name:           User's user name
        :param max_revision_id:     Maximum revision ID for the search

        :return:    User information object

        NOTE:   This method only searches active users
        """
        # Read the users that match the search attribute
        users = self.__database.tables.user_information.read_information(connection,
                                                                         "user_name",
                                                                         user_name,
                                                                         True,
                                                                         max_revision_id)

        # Return a user only if exactly one was found
        user = None

        if users is not None:
            if len(users) == 1:
                user = users[0]

        return user

    def __create_user(self,
                      connection: Connection,
                      user_name: str,
                      display_name: str,
                      email: str,
                      authentication_type: str,
                      authentication_parameters: dict,
                      revision_id: int) -> Optional[int]:
        """
        Creates a new user

        :param connection:                  Database connection
        :param user_name:                   User's user name
        :param display_name:                User's display name
        :param email:                       User's email address
        :param authentication_type:         User's authentication type
        :param authentication_parameters:   User's authentication parameters
        :param revision_id:                 Revision ID

        :return:    User ID of the newly created user
        """
        # Check if a user with the same user name already exists
        user = self.__read_user_by_user_name(connection, user_name, revision_id)

        if user is not None:
            return None

        # Create the user in the new revision
        user_id = self.__database.tables.user.insert_row(connection)

        if user_id is None:
            return None

        # Add user information to the user
        user_information_id = self.__database.tables.user_information.insert_row(connection,
                                                                                 user_id,
                                                                                 user_name,
                                                                                 display_name,
                                                                                 email,
                                                                                 True,
                                                                                 revision_id)

        if user_information_id is None:
            return None

        # Add user authentication to the user
        user_authentication_id = self.__database.tables.user_authentication.insert_row(
            connection,
            user_id,
            authentication_type)

        if user_authentication_id is None:
            return None

        reference_authentication_parameters = \
            self.__authentication.generate_reference_authentication_parameters(
                authentication_type,
                authentication_parameters)

        if reference_authentication_parameters is None:
            return None

        success = self.__database.tables.user_authentication_parameter.insert_rows(
            connection,
            user_authentication_id,
            reference_authentication_parameters)

        if not success:
            # Error, failed to add authentication parameters to the user
            return None

        return user_id

    def __read_user_authentication(self,
                                   connection: Connection,
                                   user_id: int) -> Optional[dict]:
        """
        Reads a user's authentication

        :param connection:          Database connection
        :param user_id:             ID of the user

        :return:    User authentication object
        """
        # Read the user's authentication
        user_authentication = self.__database.tables.user_authentication.read_authentication(
            connection,
            user_id)

        if user_authentication is None:
            return None

        # Read the user's authentication parameters
        authentication_parameters = \
            self.__database.tables.user_authentication_parameter.read_authentication_parameters(
                connection,
                user_authentication["id"])

        if authentication_parameters is None:
            return None

        # Create authentication object
        authentication_object = dict()
        authentication_object["user_id"] = user_authentication["user_id"]
        authentication_object["authentication_type"] = \
            user_authentication["authentication_type"]
        authentication_object["authentication_parameters"] = authentication_parameters

        return authentication_object
