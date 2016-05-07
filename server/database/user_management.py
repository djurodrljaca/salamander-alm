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

import authentication.basic
from database.database import Database
from database.connection import Connection
from typing import List, Optional


class UserManagement(object):
    """
    Class for executing user management operations on the database
    """

    def __init__(self, database_object: Database):
        """
        Constructor

        :param database_object: Database object
        """
        self.__database = database_object

    def __del__(self):
        """
        Destructor
        """
        pass

    def read_user_by_user_id(self,
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

    def read_user_by_user_name(self,
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

    def read_users_by_user_name(self,
                                connection: Connection,
                                user_name: str,
                                only_active_users: bool,
                                max_revision_id: int) -> Optional[dict]:
        """
        Reads users that matches the search parameters

        :param connection:          Database connection
        :param user_name:           User's user name
        :param only_active_users:   Only search for active users
        :param max_revision_id:     Maximum revision ID for the search

        :return:    User information object
        """
        # Read the users that match the search attribute
        users = self.__database.tables.user_information.read_information(connection,
                                                                         "user_name",
                                                                         user_name,
                                                                         only_active_users,
                                                                         max_revision_id)

        return users

    def read_users_by_display_name(self,
                                   connection: Connection,
                                   display_name: str,
                                   only_active_users: bool,
                                   max_revision_id: int) -> List[dict]:
        """
        Reads user that match the search parameters

        :param connection:          Database connection
        :param display_name:        User's display name
        :param only_active_users:   Only search for active users
        :param max_revision_id:     Maximum revision ID for the search

        :return: List of user information objects
        """
        # Read the users that match the search attribute
        users = self.__database.tables.user_information.read_information(connection,
                                                                         "display_name",
                                                                         display_name,
                                                                         only_active_users,
                                                                         max_revision_id)

        return users

    def create_user(self,
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

        :return: User ID of the newly created user
        """
        # Check if a user with the same user name already exists
        user = self.read_user_by_user_name(connection, user_name, revision_id)

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
            authentication_type,
            revision_id)

        if user_authentication_id is None:
            return None

        if authentication_type == "basic":
            # Basic authentication
            password_hash = authentication.basic.generate_password_hash(
                authentication_parameters["password"])

            user_authentication_basic_id = \
                self.__database.tables.user_authentication_basic.insert_row(connection,
                                                                            user_authentication_id,
                                                                            password_hash,
                                                                            revision_id)

            if user_authentication_basic_id is None:
                # Error, failed to add authentication information to the user
                return None
        else:
            # Error, unsupported authentication type
            return None

        return user_id

    def update_user_information(self,
                                connection: Connection,
                                user_to_modify: int,
                                user_name: str,
                                display_name: str,
                                email: str,
                                active: bool,
                                revision_id: int) -> bool:
        """
        Update user's information

        :param connection:      Database connection
        :param user_to_modify:  ID of the user that should be modified
        :param user_name:       User's user name
        :param display_name:    User's display name
        :param email:           User's email address
        :param email:           New email address of the user
        :param active:          New state of the user (active or inactive)
        :param revision_id:     Revision ID

        :return:    Success or failure
        """
        success = False

        # Check if there is already an existing user with the same user name
        user = self.read_user_by_user_name(connection, user_name, revision_id)

        if user is None:
            success = True
        elif user["user_id"] == user_to_modify:
            success = True

        if success:
            record_id = self.__database.tables.user_information.insert_row(connection,
                                                                           user_to_modify,
                                                                           user_name,
                                                                           display_name,
                                                                           email,
                                                                           active,
                                                                           revision_id)

            if record_id is None:
                success = False

        return success

    def authenticate_user(self,
                          connection: Connection,
                          user_name: str,
                          authentication_parameters: str,
                          max_revision_id: int) -> bool:
        """
        Authenticate user with basic authentication

        :param connection:                  Database connection
        :param user_name:                   User's user name
        :param authentication_parameters:   User's authentication parameters
        :param max_revision_id:             Maximum revision ID for the authentication

        :return: Authentication result: success or failure
        """
        # Find the user that matches the specified user name
        user = self.read_user_by_user_name(connection, user_name, max_revision_id)

        if user is None:
            # Error, invalid user name
            return False
        elif not user["active"]:
            # Error, user is not active
            return False

        # Authenticate user
        user_authentication = self.__database.tables.user_authentication.read_authentication(
            connection,
            user["user_id"],
            max_revision_id)

        if user_authentication is None:
            # Error, no authentication was found for that user
            return False

        user_authenticated = False

        if user_authentication["type"] == "basic":
            # Basic authentication
            password_hash = self.__database.tables.user_authentication_basic.read_password_hash(
                connection,
                user["user_id"],
                max_revision_id)

            if password_hash is not None:
                user_authenticated = authentication.basic.authenticate(
                    authentication_parameters["password"],
                    password_hash)
        else:
            # Error, unsupported authentication type
            user_authenticated = False

        return user_authenticated

    def update_user_authentication(self,
                                   connection: Connection,
                                   user_to_modify: int,
                                   authentication_type: str,
                                   authentication_parameters: dict,
                                   revision_id: int) -> bool:
        """
        Modify user's information

        :param connection:                  Database connection
        :param user_to_modify:              ID of the user that should be modified
        :param authentication_type:         User's new authentication type
        :param authentication_parameters:   User's new authentication parameters
        :param revision_id:                 Revision ID

        :return: Success or failure
        """
        # Read users current authentication type
        user_authentication = self.__database.tables.user_authentication.read_authentication(
            connection,
            user_to_modify,
            revision_id)

        if user_authentication is None:
            # Error, no authentication was found for that user
            return False

        # Modify authentication type if needed
        if authentication_type != user_authentication["type"]:
            user_authentication["id"] = self.__database.tables.user_authentication.insert_row(
                connection,
                user_to_modify,
                authentication_type,
                revision_id)

            if user_authentication["id"] is None:
                # Error, failed to modify authentication type
                return False

        # Modify authentication parameters
        if authentication_type == "basic":
            # Basic authentication
            password_hash = authentication.basic.generate_password_hash(
                authentication_parameters["password"])

            record_id = self.__database.tables.user_authentication_basic.insert_row(
                connection,
                user_authentication["id"],
                password_hash,
                revision_id)

            if record_id is None:
                # Error, failed to modify authentication information
                return False
        else:
            # Error, unsupported authentication type
            return False

        # Success
        return True
