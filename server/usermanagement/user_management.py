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

import database.database
import database.user_management
import datetime
from typing import List, Optional


class UserManagement(object):
    """
    User management
    """

    def __init__(self, database_object: database.database.Database):
        """
        Constructor

        :param database_object: Database object
        """
        self.__database = database_object
        self.__user_management = database.user_management.UserManagement(database_object)

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
            user = self.__user_management.read_user_by_user_id(connection,
                                                               user_id,
                                                               current_revision_id)

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
            user = self.__user_management.read_user_by_user_name(connection,
                                                                 user_name,
                                                                 current_revision_id)

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
            users = self.__user_management.read_users_by_user_name(connection,
                                                                   user_name,
                                                                   only_active_users,
                                                                   current_revision_id)

        return users

    def read_users_by_display_name(self,
                                   display_name: str,
                                   only_active_users = True) -> Optional[dict]:
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
            users = self.__user_management.read_users_by_display_name(connection,
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
                user_id = self.__user_management.create_user(connection,
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

            # Update user's information in the new revision
            if success:
                success = self.__user_management.update_user_information(connection,
                                                                         user_to_modify,
                                                                         user_name,
                                                                         display_name,
                                                                         email,
                                                                         active,
                                                                         revision_id)

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success

    # TODO: read authentication type

    def authenticate_user(self, user_name: str, authentication_parameters: str) -> bool:
        """
        Authenticate user with basic authentication

        :param user_name:                   User's user name
        :param authentication_parameters:   User's authentication parameters

        :return:    Success or failure
        """
        # First get the current revision
        connection = self.__database.create_connection()
        current_revision_id = self.__database.tables.revision.read_current_revision_id(connection)

        # Authenticate user
        user_authenticated = False

        if current_revision_id is not None:
            user_authenticated = self.__user_management.authenticate_user(connection,
                                                                          user_name,
                                                                          authentication_parameters,
                                                                          current_revision_id)

        return user_authenticated

    def update_user_authentication(self,
                                   requested_by_user: int,
                                   user_to_modify: int,
                                   authentication_type: str,
                                   authentication_parameters: dict) -> bool:
        """
        Update user's authentication

        :param requested_by_user:           ID of the user that requested modification of the user
        :param user_to_modify:              ID of the user that should be modified
        :param authentication_type:         User's new authentication type
        :param authentication_parameters:   User's new authentication parameters

        :return: Success or failure
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

            # Update user's authentication in the new revision
            if success:
                success = self.__user_management.update_user_authentication(
                    connection,
                    user_to_modify,
                    authentication_type,
                    authentication_parameters,
                    revision_id)

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return success
