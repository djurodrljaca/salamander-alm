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

import authentication
import authentication.basic
import database.connection
import database.tables.revision
import database.tables.user
import database.tables.user_authentication
import database.tables.user_authentication_basic
import database.tables.user_information
import sqlite3
from typing import List, Optional


# --------------------------------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------------------------------


def find_user_by_user_id(connection: sqlite3.Connection,
                         user_id: str,
                         max_revision_id: int) -> Optional[dict]:
    """
    Find a user that matches the specified user ID

    :param connection: Connection to database
    :param user_id: User id
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: User information object
    """
    # Find the users that match the search attribute
    users = database.tables.user_information.find_users_by_attribute(connection,
                                                                     "user_id",
                                                                     user_id,
                                                                     max_revision_id)

    # Return a user only if exactly one was found
    if users is not None:
        if len(users) == 1:
            return users[0]

    # Error
    return None


def find_user_by_user_name(connection: sqlite3.Connection,
                           user_name: str,
                           max_revision_id: int) -> Optional[dict]:
    """
    Find a user that matches the specified user name

    :param connection: Connection to database
    :param user_name: User name
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: User information object
    """
    # Find the users that match the search attribute
    users = database.tables.user_information.find_users_by_attribute(connection,
                                                                     "user_name",
                                                                     user_name,
                                                                     max_revision_id)

    # Return user only if exactly one user was found
    user = None
    if users is not None:
        if len(users) == 1:
            user = users[0]

    return user


def find_users_by_display_name(connection: sqlite3.Connection,
                               display_name: str,
                               max_revision_id: int) -> List[dict]:
    """
    Find user by "user name" parameter

    :param connection: Connection to database
    :param display_name: User's name in format appropriate for displaying in the GUI
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: List of user information objects
    """
    # Find all users that match the specified display name
    users = database.tables.user_information.find_users_by_attribute(connection,
                                                                     "display_name",
                                                                     display_name,
                                                                     max_revision_id)

    return users


def create_user(connection: sqlite3.Connection,
                user_name: str,
                display_name: str,
                email: str,
                authentication_type: str,
                authentication_parameters: dict,
                revision_id: int) -> Optional[int]:
    """
    Create a new user

    :param connection: Connection to database
    :param user_name: User name
    :param display_name: User's name in format appropriate for displaying in the GUI
    :param email: Email address of the user
    :param authentication_type: User's authentication type
    :param authentication_parameters: User's authentication parameters
    :param revision_id: Revision ID for for creating the new user

    :return: User ID of the newly created user
    """
    # Check if a user with the same user name already exists
    user = find_user_by_user_name(connection, user_name, revision_id)

    if user is not None:
        return None

    # Create the user in the new revision
    user_id = database.tables.user.insert_record(connection)

    if user_id is None:
        return None

    # Add user information to the user
    record_id = database.tables.user_information.insert_record(connection,
                                                               user_id,
                                                               user_name,
                                                               display_name,
                                                               email,
                                                               True,
                                                               revision_id)

    if record_id is None:
        return None

    # Add user authentication to the user
    user_authentication_id = database.tables.user_authentication.insert_record(
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

        record_id = database.tables.user_authentication_basic.insert_record(connection,
                                                                            user_authentication_id,
                                                                            password_hash,
                                                                            revision_id)

        if record_id is None:
            # Error, failed to add authentication information to the user
            return None
    else:
        # Error, unsupported authentication type
        return None

    return user_id


def modify_user_information(connection: sqlite3.Connection,
                            user_to_modify: int,
                            user_name: str,
                            display_name: str,
                            email: str,
                            active: bool,
                            revision_id: int) -> bool:
    """
    Modify user's information

    :param connection: Connection to database
    :param user_to_modify: ID of the user that should be modified
    :param user_name: New user name
    :param display_name: New user's name in format appropriate for displaying in the GUI
    :param email: New email address of the user
    :param active: New state of the user (active or inactive)
    :param revision_id: Revision ID for for creating the new user

    :return: Success or failure
    """
    # Modify user
    record_id = database.tables.user_information.insert_record(connection,
                                                               user_to_modify,
                                                               user_name,
                                                               display_name,
                                                               email,
                                                               active,
                                                               revision_id)

    return record_id is not None


def authenticate_user(connection: sqlite3.Connection,
                      user_name: str,
                      authentication_parameters: str,
                      max_revision_id: int) -> bool:
    """
    Authenticate user with basic authentication

    :param connection: Connection to database
    :param user_name: User name
    :param authentication_parameters: User's authentication parameters
    :param max_revision_id: Maximum allowed revision ID for the authentication

    :return: Authentication result: success or failure
    """
    # Find the user that matches the specified user name
    user = find_user_by_user_name(connection, user_name, max_revision_id)

    if user is None:
        # Error, invalid user name
        return False

    # Authenticate user
    user_authentication = database.tables.user_authentication.find_authentication(
        connection,
        user["user_id"],
        max_revision_id)

    if user_authentication is None:
        # Error, no authentication was found for that user
        return False

    user_authenticated = False

    if user_authentication["type"] == "basic":
        # Basic authentication
        password_hash = database.tables.user_authentication_basic.find_password_hash(
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


def modify_user_authentication(connection: sqlite3.Connection,
                               user_to_modify: int,
                               authentication_type: str,
                               authentication_parameters: dict,
                               max_revision_id: int) -> bool:
    """
    Modify user's information

    :param connection: Connection to database
    :param user_to_modify: ID of the user that should be modified
    :param authentication_type: User's new authentication type
    :param authentication_parameters: User's new authentication parameters
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: Success or failure
    """
    # Read users current authentication type
    user_authentication = database.tables.user_authentication.find_authentication(
        connection,
        user_to_modify,
        max_revision_id)

    if user_authentication is None:
        # Error, no authentication was found for that user
        return False

    # Modify authentication type if needed
    if authentication_type != user_authentication["type"]:
        user_authentication["id"] = database.tables.user_authentication.insert_record(
            connection,
            user_to_modify,
            authentication_type,
            max_revision_id)

        if user_authentication["id"] is None:
            # Error, failed to modify authentication type
            return False

    # Modify authentication parameters
    if authentication_type == "basic":
        # Basic authentication
        password_hash = authentication.basic.generate_password_hash(
            authentication_parameters["password"])

        record_id = database.tables.user_authentication_basic.insert_record(
            connection,
            user_authentication["id"],
            password_hash,
            max_revision_id)

        if record_id is None:
            # Error, failed to modify authentication information
            return False
    else:
        # Error, unsupported authentication type
        return False

    # Success
    return True

