import authentication
import authentication.basic
import datetime
import database.connection
import database.tables.revision
import database.tables.user
import database.tables.user_authentication
import database.tables.user_authentication_basic
import database.tables.user_information
import sqlite3
import typing

# TODO: add "current revision" parameter?


def create_user(requested_by_user: int,
                user_name: str,
                display_name: str,
                email: str,
                authentication_type: str,
                authentication_parameters: dict) -> int:
    """
    Create a new user with basic authentication

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

    with database.connection.create() as connection:
        # Start a new revision
        revision_id = database.tables.revision.insert_record(connection,
                                                             datetime.datetime.utcnow(),
                                                             requested_by_user)

        # Check if a user with the same user name already exists
        user = _find_user_by_user_name(connection, user_name, revision_id)

        if user is not None:
            raise ValueError("An active user with the same user name already exists")

        # Create the user in the new revision
        user_id = database.tables.user.insert_record(connection)

        # Add user information to the user
        database.tables.user_information.insert_record(connection,
                                                       user_id,
                                                       user_name,
                                                       display_name,
                                                       email,
                                                       True,
                                                       revision_id)

        # Add user authentication to the user
        user_authentication_id = database.tables.user_authentication.insert_record(
            connection,
            user_id,
            authentication_type,
            revision_id)

        if authentication_type == "basic":
            # Basic authentication
            password_hash = authentication.basic.generate_password_hash(
                authentication_parameters["password"])

            database.tables.user_authentication_basic.insert_record(
                connection,
                user_authentication_id,
                password_hash,
                revision_id)
        else:
            # Error, unsupported authentication type
            raise AttributeError("Invalid authentication type: " + type)

    return user_id


def modify_user_information(requested_by_user: int,
                            user_to_modify: int,
                            user_name: str,
                            display_name: str,
                            email: str,
                            active: bool) -> None:
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
    # Modify user
    with database.connection.create() as connection:
        # Start a new revision
        revision_id = database.tables.revision.insert_record(connection,
                                                             datetime.datetime.utcnow(),
                                                             requested_by_user)

        # Modify the user in the new revision
        database.tables.user_information.insert_record(connection,
                                                       user_to_modify,
                                                       user_name,
                                                       display_name,
                                                       email,
                                                       active,
                                                       revision_id)

    # Finished
    return


# TODO: modify user authentication


def find_user_by_user_id(user_id: int) -> dict:
    """
    Find user by "ID" parameter

    :param user_id: User ID

    :return: User ID
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = database.tables.revision.current(connection)

    # Find a user that matches the specified user ID
    user = _find_user_by_user_id(connection, user_id, revision_id)

    return user


def find_user_by_user_name(user_name: str) -> dict:
    """
    Find user by "user name" parameter

    :param user_name: User name

    :return: User information
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = database.tables.revision.current(connection)

    # Find a user that matches the specified user name
    user = _find_user_by_user_name(connection, user_name, revision_id)

    return user


def find_users_by_display_name(display_name: str) -> typing.List[dict]:
    """
    Find user by "user name" parameter

    :param display_name: User name

    :return: List of user information objects
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = database.tables.revision.current(connection)

    # Find all users that match the specified display name
    users = _find_users_by_attribute(connection, "display_name", display_name, revision_id)

    return users


def authenticate_user(user_name: str, authentication_parameters: str) -> bool:
    """
    Authenticate user with basic authentication

    :param user_name: User name
    :param authentication_parameters: User's authentication parameters

    :return: User ID
    """
    with database.connection.create() as connection:
        # First get the current revision
        revision_id = database.tables.revision.current(connection)

        # Find the user that matches the specified user name
        user = _find_user_by_user_name(connection, user_name, revision_id)

        if user is None:
            # Invalid user name
            return False

        # Authenticate user
        user_authenticated = False
        authentication_type = database.tables.user_authentication.find_authentication_type(
            connection,
            user["user_id"],
            revision_id)

        if authentication_type == "basic":
            # Basic authentication
            password_hash = database.tables.user_authentication_basic.find_password_hash(
                connection,
                user["user_id"],
                revision_id)

            if password_hash is not None:
                user_authenticated = authentication.basic.authenticate(
                    authentication_parameters["password"],
                    password_hash)
        else:
            # Error, unsupported authentication type
            raise AttributeError("Invalid authentication type: " + authentication_type)

        return user_authenticated


def _find_user_by_user_id(connection: sqlite3.Connection,
                          user_id: str,
                          max_revision_id: int) -> dict:
    """
    Find user by "user name" parameter

    :param connection: Connection to database
    :param user_id: User id
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: User ID
    """
    # Find the users that match the search attribute
    users = _find_users_by_attribute(connection, "user_id", user_id, max_revision_id)

    # Return a user only if exactly one was found
    if users is not None:
        if len(users) == 1:
            return users[0]

    # Error
    return None


def _find_user_by_user_name(connection: sqlite3.Connection,
                            user_name: str,
                            max_revision_id: int) -> dict:
    """
    Find a user that matches the specified user name

    :param connection: Connection to database
    :param user_name: User name
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: User that matches the search attribute
    """
    # Find the users that match the search attribute
    users = _find_users_by_attribute(connection, "user_name", user_name, max_revision_id)

    # Return user only if exactly one user was found
    if users is not None:
        if len(users) == 1:
            return users[0]

    # Error
    return None


def _find_users_by_attribute(connection: sqlite3.Connection,
                             attribute_name: str,
                             attribute_value: typing.Any,
                             max_revision_id: int) -> typing.List[dict]:
    """
    Find users that match the specified search attribute

    :param connection: Connection to database
    :param attribute_name: Search attribute name
    :param attribute_value: Search attribute value
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: Users that match the search attribute

    Only the following search attributes are supported:
    - user_id
    - user_name
    - display_name
    - email
    """
    # Find the users that match the search attribute
    query = ("SELECT user_id,\n"
             "       user_name,\n"
             "       display_name,\n"
             "       email,\n"
             "       revision_id\n"
             "FROM\n"
             "(\n"
             "    SELECT UI1.user_id,\n"
             "           UI1.user_name,\n"
             "           UI1.display_name,\n"
             "           UI1.email,\n"
             "           UI1.active,\n"
             "           UI1.revision_id\n"
             "    FROM user_information AS UI1\n"
             "    WHERE (UI1.revision_id =\n"
             "                (\n"
             "                    SELECT MAX(UI2.revision_id)\n"
             "                    FROM user_information AS UI2\n"
             "                    WHERE ((UI2.user_id = UI1.user_id) AND\n"
             "                           (UI2.revision_id <= :max_revision_id))\n"
             "                ))\n"
             ")\n"
             "WHERE (({0} = :attribute_value) AND\n"
             "       (active = 1))").format(attribute_name)

    cursor = connection.execute(query,
                                {"attribute_value": attribute_value,
                                 "max_revision_id": max_revision_id})

    # Process result
    users = list()

    for record in cursor.fetchall():
        if record is not None:
            user = dict(record)
            users.append(user)

    return users
