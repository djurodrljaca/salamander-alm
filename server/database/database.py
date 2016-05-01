import datetime
import sqlite3
import authentication.basic

from database.connection import Connection
from database.tables import revision
from database.tables import user, user_information, user_authentication_basic


class Database(object):
    """
    Database interface
    """

    @staticmethod
    def create_initial_database() -> None:
        """
        Creates initial database
        """
        with Connection.create() as connection:
            # Create tables and indexes
            revision.create_table(connection)
            revision.create_indexes(connection)

            user.create_table(connection)
            user.create_indexes(connection)

            user_information.create_table(connection)
            user_information.create_indexes(connection)

            user_authentication_basic.create_table(connection)
            user_authentication_basic.create_indexes(connection)

            # Create initial system users and user groups
            Database._create_initial_system_users(connection)
            Database._create_initial_system_user_groups(connection)

    @staticmethod
    def _create_initial_system_users(connection: sqlite3.Connection) -> None:
        """
        Creates the initial system users:
        - "Administrator"
        """
        # Since the database doesn't contain any users we must first create just the ID of the
        # Administrator user, then create the first revision that is referencing the Administrator
        # and then finally write all of the other user information
        user_id = user.insert_record(connection)
        revision_id = revision.insert_record(connection, datetime.datetime.utcnow(), user_id)
        user_information.insert_record(connection,
                                       user_id,
                                       "administrator",
                                       "Administrator",
                                       "",
                                       "basic",
                                       True,
                                       revision_id)
        user_authentication_basic.insert_record(
            connection,
            user_id,
            authentication.basic.generate_password_hash("administrator"),
            revision_id)

    @staticmethod
    def _create_initial_system_user_groups(connection: sqlite3.Connection) -> None:
        """
        Creates the initial system users:
        - "Administrators"
        """
        # TODO: implement
        return
