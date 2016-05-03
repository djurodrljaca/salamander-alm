import authentication.basic
import datetime
import database.connection
import database.tables.revision
import database.tables.user
import database.tables.user_authentication
import database.tables.user_authentication_basic
import database.tables.user_information
import sqlite3


def create_initial_database() -> None:
    """
    Creates initial database
    """
    with database.connection.create() as connection:
        # Create tables and indexes
        database.tables.revision.create_table(connection)
        database.tables.revision.create_indexes(connection)

        database.tables.user.create_table(connection)
        database.tables.user.create_indexes(connection)

        database.tables.user_authentication.create_table(connection)
        database.tables.user_authentication.create_indexes(connection)

        database.tables.user_authentication_basic.create_table(connection)
        database.tables.user_authentication_basic.create_indexes(connection)

        database.tables.user_information.create_table(connection)
        database.tables.user_information.create_indexes(connection)

        # Create initial system users and user groups
        _create_initial_system_users(connection)
        _create_initial_system_user_groups(connection)


def _create_initial_system_users(connection: sqlite3.Connection) -> None:
    """
    Creates the initial system users:
    - "Administrator"
    """
    # Since the database doesn't contain any users we must first create just the ID of the
    # Administrator user, then create the first revision that is referencing the Administrator
    # and then finally write all of the other user information
    user_id = database.tables.user.insert_record(connection)
    revision_id = database.tables.revision.insert_record(connection,
                                                         datetime.datetime.utcnow(),
                                                         user_id)
    database.tables.user_information.insert_record(connection,
                                                   user_id,
                                                   "administrator",
                                                   "Administrator",
                                                   "",
                                                   True,
                                                   revision_id)

    user_authentication_id = database.tables.user_authentication.insert_record(
        connection,
        user_id,
        "basic",
        revision_id)

    database.tables.user_authentication_basic.insert_record(
        connection,
        user_authentication_id,
        authentication.basic.generate_password_hash("administrator"),
        revision_id)


def _create_initial_system_user_groups(connection: sqlite3.Connection) -> None:
    """
    Creates the initial system users:
    - "Administrators"
    """
    # TODO: implement
    return

