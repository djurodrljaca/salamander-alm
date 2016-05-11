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
from database.tables.user import UserSelection
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
    def read_all_user_ids(user_selection=UserSelection.Active) -> List[int]:
        """
        Reads all user IDs from the database

        :param user_selection:  Search for active, inactive or all users

        :return:    List of user IDs
        """
        connection = DatabaseInterface.create_connection()
        return DatabaseInterface.tables().user.read_all_ids(connection, user_selection)

    @staticmethod
    def read_user_by_id(user_id: int) -> Optional[dict]:
        """
        Reads a user (active or inactive) that matches the specified user ID

        :param user_id: ID of the user

        :return:    User information object
        """
        connection = DatabaseInterface.create_connection()

        return UserManagementInterface.__read_user_by_id(connection, user_id)

    @staticmethod
    def read_user_by_user_name(user_name: str) -> Optional[dict]:
        """
        Reads an active user that matches the specified user name

        :param user_name:   User's user name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        connection = DatabaseInterface.create_connection()

        return UserManagementInterface.__read_user_by_user_name(connection, user_name)

    @staticmethod
    def read_users_by_user_name(user_name: str) -> List[dict]:
        """
        Reads all active and inactive users that match the specified user name

        :param user_name:   User's user name

        :return:    User information of all users that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        connection = DatabaseInterface.create_connection()

        return DatabaseInterface.tables().user.read_users_by_attribute(connection,
                                                                       "user_name",
                                                                       user_name,
                                                                       UserSelection.All)

    @staticmethod
    def read_user_by_display_name(display_name: str) -> Optional[dict]:
        """
        Reads an active user that matches the specified display name

        :param display_name:    User's display name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        connection = DatabaseInterface.create_connection()

        return UserManagementInterface.__read_user_by_display_name(connection, display_name)

    @staticmethod
    def read_users_by_display_name(display_name: str) -> List[dict]:
        """
        Reads all active and inactive users that match the specified display name

        :param display_name:    User's display name

        :return:    User information of all users that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        connection = DatabaseInterface.create_connection()

        return DatabaseInterface.tables().user.read_users_by_attribute(connection,
                                                                       "display_name",
                                                                       display_name,
                                                                       UserSelection.All)

    @staticmethod
    def create_user(user_name: str,
                    display_name: str,
                    email: str,
                    authentication_type: str,
                    authentication_parameters: dict) -> Optional[int]:
        """
        Creates a new user

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

            # Create the user
            if success:
                user_id = UserManagementInterface.__create_user(connection,
                                                                user_name,
                                                                display_name,
                                                                email,
                                                                authentication_type,
                                                                authentication_parameters)

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
    def update_user_information(user_to_modify: int,
                                user_name: str,
                                display_name: str,
                                email: str,
                                active: bool) -> bool:
        """
        Updates user's information

        :param user_to_modify:  ID of the user that should be modified
        :param user_name:       User's new user name
        :param display_name:    User's new display name
        :param email:           User's new email address
        :param active:          User's new state (active or inactive)

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Check if there is already an existing user with the same user name
            if success:
                user = UserManagementInterface.__read_user_by_user_name(connection, user_name)

                if user is not None:
                    if user["id"] != user_to_modify:
                        success = False

            # Check if there is already an existing user with the same display name
            if success:
                user = UserManagementInterface.__read_user_by_display_name(connection,
                                                                           display_name)

                if user is not None:
                    if user["id"] != user_to_modify:
                        success = False

            # Update user's information
            if success:
                success = DatabaseInterface.tables().user.update_row(connection,
                                                                     user_to_modify,
                                                                     user_name,
                                                                     display_name,
                                                                     email,
                                                                     active)

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success

    @staticmethod
    def activate_user(user_id: int) -> bool:
        """
        Activates an inactive user

        :param user_id: ID of the user that should be activated

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Read user
            user = None

            if success:
                user = UserManagementInterface.__read_user_by_id(connection, user_id)

                if user is None:
                    success = False
                elif user["active"]:
                    # Error, user is already active
                    success = False

            # Activate user
            if success:
                success = DatabaseInterface.tables().user.update_row(connection,
                                                                     user_id,
                                                                     user["user_name"],
                                                                     user["display_name"],
                                                                     user["email"],
                                                                     True)

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success

    @staticmethod
    def deactivate_user(user_id: int) -> bool:
        """
        Deactivates an active user

        :param user_id: ID of the user that should be deactivated

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Read user
            user = None

            if success:
                user = UserManagementInterface.__read_user_by_id(connection, user_id)

                if user is None:
                    success = False
                elif not user["active"]:
                    # Error, user is already inactive
                    success = False

            # Deactivate user
            if success:
                success = DatabaseInterface.tables().user.update_row(connection,
                                                                     user_id,
                                                                     user["user_name"],
                                                                     user["display_name"],
                                                                     user["email"],
                                                                     False)

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
        Reads user's authentication

        :param user_id: ID of the user

        :return:    User authentication object

        Returned dictionary contains items:

        - authentication_type
        - authentication_parameters
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
    def authenticate_user(user_name: str, authentication_parameters: dict) -> Optional[int]:
        """
        Authenticates a user

        :param user_name:                   User's user name
        :param authentication_parameters:   User's authentication parameters

        :return:    ID of the authenticated user
        """
        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            user = None

            if success:
                user = UserManagementInterface.__read_user_by_user_name(connection, user_name)

                if user is None:
                    # Error, invalid user name
                    success = False

            # Read user's authentication information
            user_authentication = None

            if success:
                user_authentication = UserManagementInterface.__read_user_authentication(
                    connection,
                    user["id"])

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

        if user_authenticated:
            return user["id"]
        else:
            return None

    @staticmethod
    def update_user_authentication(user_to_modify: int,
                                   authentication_type: str,
                                   authentication_parameters: dict) -> bool:
        """
        Updates user's authentication

        :param user_to_modify:              ID of the user that should be modified
        :param authentication_type:         User's new authentication type
        :param authentication_parameters:   User's new authentication parameters

        :return:    Success or failure
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
                success = DatabaseInterface.tables().user_authentication.update_row(
                    connection,
                    user_to_modify,
                    authentication_type)

            # Modify authentication parameters
            reference_authentication_parameters = None

            if success:
                DatabaseInterface.tables().user_authentication_parameter.delete_rows(connection,
                                                                                     user_to_modify)

                reference_authentication_parameters = \
                    AuthenticationInterface.generate_reference_authentication_parameters(
                        authentication_type,
                        authentication_parameters)

                if reference_authentication_parameters is None:
                    success = False

            if success:
                success = DatabaseInterface.tables().user_authentication_parameter.insert_rows(
                    connection,
                    user_to_modify,
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
    def __read_user_by_id(connection: Connection, user_id: int) -> Optional[dict]:
        """
        Reads a user (active or inactive) that matches the search parameters

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        # Read the users that match the search attribute
        users = DatabaseInterface.tables().user.read_users_by_attribute(connection,
                                                                        "id",
                                                                        user_id,
                                                                        UserSelection.All)

        # Return a user only if exactly one was found
        user = None

        if users is not None:
            if len(users) == 1:
                user = users[0]

        return user

    @staticmethod
    def __read_user_by_user_name(connection: Connection, user_name: str) -> Optional[dict]:
        """
        Reads an active user that matches the specified user name

        :param user_name:   User's user name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        # Read the users that match the search attribute
        users = DatabaseInterface.tables().user.read_users_by_attribute(connection,
                                                                        "user_name",
                                                                        user_name,
                                                                        UserSelection.Active)

        # Return a user only if exactly one was found
        user = None

        if users is not None:
            if len(users) == 1:
                user = users[0]

        return user

    @staticmethod
    def __read_user_by_display_name(connection: Connection, display_name: str) -> Optional[dict]:
        """
        Reads an active user that matches the specified display name

        :param display_name:    User's display name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        # Read the users that match the search attribute
        users = DatabaseInterface.tables().user.read_users_by_attribute(connection,
                                                                        "display_name",
                                                                        display_name,
                                                                        UserSelection.Active)

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
                      authentication_parameters: dict) -> Optional[int]:
        """
        Creates a new user

        :param connection:                  Database connection
        :param user_name:                   User's user name
        :param display_name:                User's display name
        :param email:                       User's email address
        :param authentication_type:         User's authentication type
        :param authentication_parameters:   User's authentication parameters

        :return:    User ID of the newly created user
        """
        # Check if a user with the same user name already exists
        user = UserManagementInterface.__read_user_by_user_name(connection, user_name)

        if user is not None:
            return None

        # Check if a user with the same display name already exists
        user = UserManagementInterface.__read_user_by_display_name(connection, display_name)

        if user is not None:
            return None

        # Create the user in the new revision
        user_id = DatabaseInterface.tables().user.insert_row(connection,
                                                             user_name,
                                                             display_name,
                                                             email,
                                                             True)

        if user_id is None:
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
            user_id,
            reference_authentication_parameters)

        if not success:
            # Error, failed to add authentication parameters to the user
            return None

        return user_id

    @staticmethod
    def __read_user_authentication(connection: Connection, user_id: int) -> Optional[dict]:
        """
        Reads user's authentication

        :param connection:  Database connection
        :param user_id:     ID of the user

        :return:    User authentication object

        Returned dictionary contains items:

        - authentication_type
        - authentication_parameters
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
                user_id)

        if authentication_parameters is None:
            return None

        # Create authentication object
        authentication_object = dict()
        authentication_object["authentication_type"] = user_authentication["authentication_type"]
        authentication_object["authentication_parameters"] = authentication_parameters

        return authentication_object
