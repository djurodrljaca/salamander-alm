import authentication.basic
import datetime
import database.connection

from database.tables import revision
from database.tables import user, user_information, user_authentication_basic


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
    # Check if a user with the same user name already exists
    existing_user_id = find_user_by_user_name(user_name)

    if existing_user_id is not None:
        raise ValueError("An active user with the same user name already exists")

    # Create a new user
    with database.connection.create() as connection:
        # Start a new revision
        revision_id = revision.insert_record(connection,
                                             datetime.datetime.utcnow(),
                                             requested_by_user)

        # Create the user in the new revision
        user_id = user.insert_record(connection)
        user_information.insert_record(connection,
                                       user_id,
                                       user_name,
                                       display_name,
                                       email,
                                       "basic",
                                       True,
                                       revision_id)
        user_authentication_basic.insert_record(
            connection,
            user_id,
            authentication.basic.generate_password_hash(password),
            revision_id)

    return user_id


def find_user_by_user_name(user_name: str) -> int:
    """
    Find user by "user name" parameter

    :param user_name: User name

    :return: User ID
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = revision.current(connection)

    cursor = connection.execute(
        "SELECT user.id, MAX(user_information.revision_id) FROM user\n"
        "INNER JOIN user_information\n"
        "    ON ((user.id = user_information.user_id) AND\n"
        "        (user_information.active = 1) AND\n"
        "        (user_information.user_name = ?))\n"
        "WHERE (user_information.revision_id <= ?);",
        (user_name, revision_id))

    record = cursor.fetchone()

    if record is not None:
        return record[0]

    return None


def find_users_by_display_name(display_name: str) -> list:
    """
    Find user by "user name" parameter

    :param display_name: User name

    :return: List of user IDs
    """
    # First get the current revision
    connection = database.connection.create()
    revision_id = revision.current(connection)

    cursor = connection.execute(
        "SELECT user.id FROM user\n"
        "INNER JOIN user_information\n"
        "    ON ((user.id = user_information.user_id) AND\n"
        "        (user_information.active = 1) AND\n"
        "        (user_information.display_name = ?))\n"
        "WHERE (user_information.revision_id <= ?) AND\n"
        "      (user_information.revision_id = (SELECT MAX(user_information.revision_id)"
        "                                       FROM user_information"
        "                                       WHERE (user_information.user_id = user.id)));",
        (display_name, revision_id))

    user_ids = list()

    for record in cursor.fetchall():
        if record is not None:
            user_ids.append(record[0])

    return user_ids


# TODO: authenticate user
