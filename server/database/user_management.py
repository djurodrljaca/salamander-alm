import authentication.basic
import datetime
import database.connection
import sqlite3
import database.tables


def create_user_basic_authentication(requested_by_user: int,
                                     user_name: str,
                                     display_name: str,
                                     email: str,
                                     password: str) -> int:
    """
    Create a new user with basic authentication

    :param requested_by_user: ID of the user that requested creation of the new user
    :param user_name: User name
    :param display_name: User's name in format appropriate for displaying in the GUI
    :param email: Email address of the user
    :param password: User's password

    :return: User ID of the new user
    """
    # Create a new user
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
        database.tables.user_information.insert_record(connection,
                                                       user_id,
                                                       user_name,
                                                       display_name,
                                                       email,
                                                       "basic",
                                                       True,
                                                       revision_id)
        database.tables.user_authentication_basic.insert_record(
            connection,
            user_id,
            authentication.basic.generate_password_hash(password),
            revision_id)

    return user_id


# TODO: modify user information
# TODO: modify user authentication


def find_user_by_user_name(user_name: str) -> dict:
    """
    Find user by "user name" parameter

    :param user_name: User name

    :return: User ID
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = database.tables.revision.current(connection)

    # Find the user that matches the specified user name
    user = _find_user_by_user_name(connection, user_name, revision_id)

    return user


def find_users_by_display_name(display_name: str) -> list:
    """
    Find user by "user name" parameter

    :param display_name: User name

    :return: List of user IDs
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = database.tables.revision.current(connection)

    # Find all users that match the specifed display name
    cursor = connection.execute(
        "SELECT U.id AS id,\n"
        "       UI1.user_id AS user_id,\n"
        "       UI1.user_name AS user_name,\n"
        "       UI1.display_name AS display_name,\n"
        "       UI1.email AS email,\n"
        "       UI1.authentication_method AS authentication_method\n"
        "FROM user AS U INNER JOIN\n"
        "(\n"
        "    SELECT UI2.user_id,\n"
        "           UI2.user_name,\n"
        "           UI2.display_name,\n"
        "           UI2.email,\n"
        "           UI2.authentication_method,\n"
        "           UI2.revision_id\n"
        "    FROM user_information AS UI2\n"
        "    WHERE (UI2.active = 1) AND\n"
        "          (UI2.display_name = :display_name) AND\n"
        "          (UI2.revision_id <= :max_revision_id) AND\n"
        "          (UI2.revision_id =\n"
        "              (\n"
        "                  SELECT MAX(UI3.revision_id)\n"
        "                  FROM user_information AS UI3\n"
        "                  WHERE (UI3.user_id = UI2.user_id)\n"
        "              ))\n"
        ") AS UI1\n"
        "ON (U.id = UI1.user_id);\n",
        {"display_name": display_name, "max_revision_id": revision_id})

    users = list()

    # Process results
    for record in cursor.fetchall():
        if record is not None:
            user = dict(record)
            users.append(user)

    return users


def authenticate_user_basic_authentication(user_name: str, password: str) -> bool:
    """
    Authenticate user with basic authentication

    :param user_name: User name
    :param password: Password provided for authentication

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

        if user["authentication_method"] != "basic":
            # Invalid authentication method
            return False

        # Find the user password for the user that matches the specified user ID
        password_hash = database.tables.user_authentication_basic.find_password_hash(connection,
                                                                                     user["id"],
                                                                                     revision_id)

        if password_hash is None:
            # Password was not found for the selected
            return False

        # Authenticate user
        return authentication.basic.authenticate(password, password_hash)

    return False


def _find_user_by_user_name(connection: sqlite3.Connection,
                            user_name: str,
                            max_revision_id: int) -> dict:
    """
    Find user by "user name" parameter

    :param connection: Connection to database
    :param user_name: User name
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: User ID
    """
    # Find the user that matches the specified user name
    cursor = connection.execute(
        "SELECT U.id AS id,\n"
        "       UI1.user_id AS user_id,\n"
        "       UI1.user_name AS user_name,\n"
        "       UI1.display_name AS display_name,\n"
        "       UI1.email AS email,\n"
        "       UI1.authentication_method AS authentication_method\n"
        "FROM user AS U INNER JOIN\n"
        "(\n"
        "    SELECT UI2.user_id,\n"
        "           UI2.user_name,\n"
        "           UI2.display_name,\n"
        "           UI2.email,\n"
        "           UI2.authentication_method,\n"
        "           UI2.revision_id\n"
        "    FROM user_information AS UI2\n"
        "    WHERE (UI2.active = 1) AND\n"
        "          (UI2.user_name = :user_name) AND\n"
        "          (UI2.revision_id <= :max_revision_id) AND\n"
        "          (UI2.revision_id =\n"
        "              (\n"
        "                  SELECT MAX(UI3.revision_id)\n"
        "                  FROM user_information AS UI3\n"
        "                  WHERE (UI3.user_id = UI2.user_id)\n"
        "              ))\n"
        ") AS UI1\n"
        "ON (U.id = UI1.user_id)\n",
        {"user_name": user_name, "max_revision_id": max_revision_id})

    # Process result
    record = cursor.fetchone()

    if record is not None:
        user = dict(record)
        return user

    return None
