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
import database.connection
import database.tables.revision
import database.user_management
from typing import List, Optional
import sys


# --------------------------------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------------------------------
# TODO: search also for disabled users? Add a parameter for this?
# TODO: rename the "find" API to "get"?


def find_user_by_user_id(user_id: int) -> Optional[dict]:
    """
    Find a user that matches the specified user ID

    :param user_id: User ID

    :return: User information object
    """
    # First get the current revision
    connection = database.connection.create()
    current_revision_id = database.tables.revision.current(connection.native_connection)

    # Find a user that matches the specified user ID
    user = None

    if current_revision_id is not None:
        user = database.user_management.find_user_by_user_id(connection.native_connection,
                                                             user_id,
                                                             current_revision_id)

    return user


def find_user_by_user_name(user_name: str) -> Optional[dict]:
    """
    Find a user that matches the specified user name

    :param user_name: User name

    :return: User information object
    """
    # First get the current revision
    connection = database.connection.create()
    current_revision_id = database.tables.revision.current(connection.native_connection)

    # Find a user that matches the specified user ID
    user = None

    if current_revision_id is not None:
        user = database.user_management.find_user_by_user_name(connection.native_connection,
                                                               user_name,
                                                               current_revision_id)

    return user


def find_users_by_display_name(display_name: str) -> List[dict]:
    """
    Find user by "user name" parameter

    :param display_name: User's name in format appropriate for displaying in the GUI

    :return: List of user information objects
    """
    # First get the current revision
    connection = database.connection.create()
    current_revision_id = database.tables.revision.current(connection.native_connection)

    # Find all users that match the specified display name
    users = list()

    if current_revision_id is not None:
        users = database.user_management.find_users_by_display_name(connection.native_connection,
                                                                    display_name,
                                                                    current_revision_id)

    return users


def create_user(requested_by_user: int,
                user_name: str,
                display_name: str,
                email: str,
                authentication_type: str,
                authentication_parameters: dict) -> Optional[int]:
    """
    Create a new user

    :param requested_by_user: ID of the user that requested creation of the new user
    :param user_name: User name
    :param display_name: User's name in format appropriate for displaying in the GUI
    :param email: Email address of the user
    :param authentication_type: User's authentication type
    :param authentication_parameters: User's authentication parameters

    :return: User ID of the new user
    """
    # Create a new user
    user_id = None

    connection = database.connection.create()

    try:
        success = connection.begin()

        # Start a new revision
        revision_id = None

        if success:
            revision_id = database.tables.revision.insert_record(connection.native_connection,
                                                                 datetime.datetime.utcnow(),
                                                                 requested_by_user)

            if revision_id is None:
                success = False

        # Create the user
        if success:
            user_id = database.user_management.create_user(connection.native_connection,
                                                           user_name,
                                                           display_name,
                                                           email,
                                                           authentication_type,
                                                           authentication_parameters,
                                                           revision_id)

            if user_id is None:
                success = False

        if success:
            connection.commit()
        else:
            connection.rollback()
    except:
        connection.rollback()
        raise sys.exc_info()[0]

    return user_id


def modify_user_information(requested_by_user: int,
                            user_to_modify: int,
                            user_name: str,
                            display_name: str,
                            email: str,
                            active: bool) -> bool:
    """
    Modify user's information

    :param requested_by_user: ID of the user that requested modification of a user
    :param user_to_modify: ID of the user that should be modified
    :param user_name: New user name
    :param display_name: New user's name in format appropriate for displaying in the GUI
    :param email: New email address of the user
    :param active: New state of the user (active or inactive)

    :return: Success or failure
    """
    # Modify user's information
    connection = database.connection.create()

    try:
        success = connection.begin()

        # Start a new revision
        revision_id = None

        if success:
            revision_id = database.tables.revision.insert_record(connection.native_connection,
                                                                 datetime.datetime.utcnow(),
                                                                 requested_by_user)

            if revision_id is None:
                success = False

        # Modify user's information in the new revision
        if success:
            success = database.user_management.modify_user_information(connection.native_connection,
                                                                       user_to_modify,
                                                                       user_name,
                                                                       display_name,
                                                                       email,
                                                                       active,
                                                                       revision_id)

        if success:
            connection.commit()
        else:
            connection.rollback()
    except:
        connection.rollback()
        raise sys.exc_info()[0]

    return success


def authenticate_user(user_name: str, authentication_parameters: str) -> bool:
    """
    Authenticate user with basic authentication

    :param user_name: User name
    :param authentication_parameters: User's authentication parameters

    :return: User ID
    """
    # First get the current revision
    connection = database.connection.create()
    current_revision_id = database.tables.revision.current(connection.native_connection)

    # Authenticate user
    user_authenticated = False

    if current_revision_id is not None:
        user_authenticated = database.user_management.authenticate_user(
            connection.native_connection,
            user_name,
            authentication_parameters,
            current_revision_id)

    return user_authenticated


def modify_user_authentication(requested_by_user: int,
                               user_to_modify: int,
                               authentication_type: str,
                               authentication_parameters: dict) -> bool:
    """
    Modify user's authentication

    :param requested_by_user: ID of the user that requested modification of a user
    :param user_to_modify: ID of the user that should be modified
    :param authentication_type: User's new authentication type
    :param authentication_parameters: User's new authentication parameters

    :return: Success or failure
    """
    # Modify user's authentication
    connection = database.connection.create()

    try:
        success = connection.begin()

        # Start a new revision
        revision_id = None

        if success:
            revision_id = database.tables.revision.insert_record(connection.native_connection,
                                                                 datetime.datetime.utcnow(),
                                                                 requested_by_user)

            if revision_id is None:
                success = False

        # Modify user's authentication in the new revision
        if success:
            success = database.user_management.modify_user_authentication(
                connection.native_connection,
                user_to_modify,
                authentication_type,
                authentication_parameters,
                revision_id)

        if success:
            connection.commit()
        else:
            connection.rollback()
    except:
        connection.rollback()
        raise sys.exc_info()[0]

    return success
