import sqlite3
import os
import os.path


# File path to the database
_file_path = "database.db"


class Connection(object):
    """
    Database connection
    """

    @staticmethod
    def delete_database() -> None:
        """
        Deletes the database
        """
        if os.path.exists(_file_path):
            os.remove(_file_path)

    @staticmethod
    def create() -> sqlite3.Connection:
        """
        Creates a connection to the database

        :return: Database connection
        """
        return sqlite3.connect(_file_path)
