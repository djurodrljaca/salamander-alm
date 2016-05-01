import os
import os.path
import sqlite3


# File path to the database
_file_path = "database.db"


def delete_database() -> None:
    """
    Deletes the database
    """
    if os.path.exists(_file_path):
        os.remove(_file_path)


def create() -> sqlite3.Connection:
    """
    Creates a connection to the database

    :return: Database connection
    """
    connection = sqlite3.connect(_file_path)
    connection.row_factory = sqlite3.Row

    return connection
