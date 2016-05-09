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
from database.database import DatabaseInterface
import datetime
from typing import List, Optional


class UserManagementInterface(object):
    """
    User management

    Dependencies:
    - AuthenticationInterface
    - DatabaseInterface
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def __del__(self):
        """
        Destructor
        """
        pass

    @staticmethod
    def read_all_user_ids() -> List[int]:
        """
        Reads all user IDs from the database

        :return:    List of user IDs

        NOTE:   This method searches both active and inactive users
        """
        connection = DatabaseInterface.create_connection()
        return DatabaseInterface.tables().user.read_all_users(connection)

    @staticmethod
    def read_user_by_id(user_id: int) -> Optional[dict]:
        """
        Reads a user that matches the specified user ID

        :param user_id: ID of the user

        :return:    User information object

        NOTE:   This method searches both active and inactive users
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read a user that matches the specified user ID
        user = None

        if current_revision_id is not None:
            user = UserManagementInterface.__read_user_by_id(connection,
                                                             user_id,
                                                             current_revision_id)

        return user

    @staticmethod
    def read_user_by_user_name(user_name: str) -> Optional[dict]:
        """
        Reads a user that matches the specified user name

        :param user_name:   User's user name

        :return:    User information object

        NOTE:   This method only searches active users
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read a user that matches the specified user name
        user = None

        if current_revision_id is not None:
            user = UserManagementInterface.__read_user_by_user_name(connection,
                                                                    user_name,
                                                                    current_revision_id)

        return user

    @staticmethod
    def read_users_by_user_name(user_name: str, only_active_users: bool) -> List[dict]:
        """
        Reads a user that matches the specified user name

        :param user_name:           User's user name
        :param only_active_users:   Only search for active users

        :return:    User information object
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read users that match the specified user name
        users = list()

        if current_revision_id is not None:
            users = DatabaseInterface.tables().user_information.read_information(
                connection,
                "user_name",
                user_name,
                only_active_users,
                current_revision_id)

        return users

    @staticmethod
    def read_users_by_display_name(display_name: str, only_active_users=True) -> List[dict]:
        """
        Reads a user that matches the specified display name

        :param display_name:        User's display name
        :param only_active_users:   Only search for active users

        :return:    User information object
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read users that match the specified display name
        users = list()

        if current_revision_id is not None:
            users = DatabaseInterface.tables().user_information.read_information(
                connection,
                "display_name",
                display_name,
                only_active_users,
                current_revision_id)

        return users

    @staticmethod
    def create_user(requested_by_user: int,
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

        :return:    User ID of the new user
        """
        user_id = None
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Start a new revision
            revision_id = None

            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)

                if revision_id is None:
                    success = False

            # Create the user
            if success:
                user_id = UserManagementInterface.__create_user(connection,
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

    @staticmethod
    def update_user_information(requested_by_user: int,
                                user_to_modify: int,
                                user_name: str,
                                display_name: str,
                                email: str,
                                active: bool) -> bool:
        """
        Update user's information

        :param requested_by_user:   ID of the user that requested modification of the user
        :param user_to_modify:      ID of the user that should be modified
        :param user_name:           User's new user name
        :param display_name:        User's new display name
        :param email:               User's new email address
        :param active:              User's new state (active or inactive)

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Start a new revision
            revision_id = None

            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)

                if revision_id is None:
                    success = False

            # Check if there is already an existing user with the same user name
            if success:
                user = UserManagementInterface.__read_user_by_user_name(connection,
                                                                        user_name,
                                                                        revision_id)

                if user is not None:
                    if user["user_id"] != user_to_modify:
                        success = False

            # Update user's information in the new revision
            if success:
                row_id = DatabaseInterface.tables().user_information.insert_row(connection,
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

    @staticmethod
    def read_user_authentication(user_id: int) -> Optional[dict]:
        """
        Reads a user's authentication

        :param user_id: ID of the user

        :return:    User authentication object
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Read the user's authentication
            user_authentication = None

            if success:
                user_authentication = UserManagementInterface.__read_user_authentication(connection,
                                                                                         user_id)

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

    @staticmethod
    def authenticate_user(user_name: str, authentication_parameters: str) -> bool:
        """
        Authenticate user

        :param user_name:                   User's user name
        :param authentication_parameters:   User's authentication parameters

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Read the user that matches the specified user name
            if success:
                current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                    connection)

                if current_revision_id is None:
                    success = False

            user = None

            if success:
                user = UserManagementInterface.__read_user_by_user_name(connection,
                                                                        user_name,
                                                                        current_revision_id)

                if user is None:
                    # Error, invalid user name
                    success = False
                elif not user["active"]:
                    # Error, user is not active
                    success = False

            # Read user's authentication information
            if success:
                user_authentication = UserManagementInterface.__read_user_authentication(
                    connection,
                    user["user_id"])

                if user_authentication is None:
                    # Error, no authentication was found for that user
                    success = False

            # Authenticate user
            user_authenticated = False

            if success:
                user_authenticated = AuthenticationInterface.authenticate(
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

    @staticmethod
    def update_user_authentication(user_to_modify: int,
                                   authentication_type: str,
                                   authentication_parameters: dict) -> bool:
        """
        Update user's authentication

        :param user_to_modify:              ID of the user that should be modified
        :param authentication_type:         User's new authentication type
        :param authentication_parameters:   User's new authentication parameters

        :return: Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Update user's authentication
            user_authentication = None

            if success:
                # Read users current authentication information
                user_authentication = \
                    DatabaseInterface.tables().user_authentication.read_authentication(
                        connection,
                        user_to_modify)

                if user_authentication is None:
                    # Error, no authentication was found for that user
                    success = False

            # Modify authentication type if needed
            if success and (authentication_type != user_authentication["authentication_type"]):
                success = DatabaseInterface.tables().user_authentication.update_authentication_type(
                    connection,
                    user_authentication["id"],
                    authentication_type)

            # Modify authentication parameters
            if success:
                success = False
                DatabaseInterface.tables().user_authentication_parameter.delete_rows(
                    connection,
                    user_authentication["id"])

                reference_authentication_parameters = \
                    AuthenticationInterface.generate_reference_authentication_parameters(
                        authentication_type,
                        authentication_parameters)

                if reference_authentication_parameters is not None:
                    success = DatabaseInterface.tables().user_authentication_parameter.insert_rows(
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

    @staticmethod
    def __read_user_by_id(connection: Connection,
                          user_id: int,
                          max_revision_id: int) -> Optional[dict]:
        """
        Reads a user that matches the search parameters

        :param connection:      Database connection
        :param user_id:         ID of the user
        :param max_revision_id: Maximum revision ID for the search

        :return:    User information object
        """
        # Read the users that match the search attribute
        users = DatabaseInterface.tables().user_information.read_information(connection,
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

    @staticmethod
    def __read_user_by_user_name(connection: Connection,
                                 user_name: str,
                                 max_revision_id: int) -> Optional[dict]:
        """
        Reads a user that matches the search parameters

        :param connection:      Database connection
        :param user_name:       User's user name
        :param max_revision_id: Maximum revision ID for the search

        :return:    User information object

        NOTE:   This method only searches active users
        """
        # Read the users that match the search attribute
        users = DatabaseInterface.tables().user_information.read_information(connection,
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

    @staticmethod
    def __create_user(connection: Connection,
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
        user = UserManagementInterface.__read_user_by_user_name(connection, user_name, revision_id)

        if user is not None:
            return None

        # Create the user in the new revision
        user_id = DatabaseInterface.tables().user.insert_row(connection)

        if user_id is None:
            return None

        # Add user information to the user
        user_information_id = DatabaseInterface.tables().user_information.insert_row(connection,
                                                                                     user_id,
                                                                                     user_name,
                                                                                     display_name,
                                                                                     email,
                                                                                     True,
                                                                                     revision_id)

        if user_information_id is None:
            return None

        # Add user authentication to the user
        user_authentication_id = DatabaseInterface.tables().user_authentication.insert_row(
            connection,
            user_id,
            authentication_type)

        if user_authentication_id is None:
            return None

        reference_authentication_parameters = \
            AuthenticationInterface.generate_reference_authentication_parameters(
                authentication_type,
                authentication_parameters)

        if reference_authentication_parameters is None:
            return None

        success = DatabaseInterface.tables().user_authentication_parameter.insert_rows(
            connection,
            user_authentication_id,
            reference_authentication_parameters)

        if not success:
            # Error, failed to add authentication parameters to the user
            return None

        return user_id

    @staticmethod
    def __read_user_authentication(connection: Connection,
                                   user_id: int) -> Optional[dict]:
        """
        Reads a user's authentication

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    User authentication object
        """
        # Read the user's authentication
        user_authentication = DatabaseInterface.tables().user_authentication.read_authentication(
            connection,
            user_id)

        if user_authentication is None:
            return None

        # Read the user's authentication parameters
        authentication_parameters = \
            DatabaseInterface.tables().user_authentication_parameter.read_authentication_parameters(
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
