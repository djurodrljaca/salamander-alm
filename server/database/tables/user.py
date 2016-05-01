import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "user"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE user (\n"
        "    id INTEGER PRIMARY KEY AUTOINCREMENT\n"
        "             NOT NULL\n"
        ");")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user"

    :param connection: Connection to database
    """
    return


def insert_record(connection: sqlite3.Connection) -> int:
    """
    Inserts a new record in the table: "user"

    :param connection: Connection to database

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user (id)\n"
        "VALUES (NULL);")

    return cursor.lastrowid
