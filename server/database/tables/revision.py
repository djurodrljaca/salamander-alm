import datetime
import sqlite3
import database.datatypes


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "revision"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE revision (\n"
        "    id        INTEGER  PRIMARY KEY AUTOINCREMENT\n"
        "                       NOT NULL,\n"
        "    timestamp DATETIME,\n"
        "    user_id   INTEGER  REFERENCES user (id) \n"
        ");")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "revision"

    :param connection: Connection to database
    """
    return


def current(connection: sqlite3.Connection) -> int:
    """
    Get current revision number

    :param connection: Connection to database

    :return: Current revision number
    """
    cursor = connection.execute("SELECT MAX(id) FROM revision;")

    record = cursor.fetchone()

    if record is not None:
        return record[0]

    return None


def insert_record(connection: sqlite3.Connection,
                  timestamp: datetime.datetime,
                  user_id: int) -> int:
    """
    Inserts a new record in the table: "revision"

    :param connection: Connection to database
    :param timestamp: Timestamp of when the revision was created
    :param user_id: ID of the user that created the revision

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO revision (id, timestamp, user_id)\n"
        "VALUES (NULL, ?, ?);",
        (database.datatypes.datetime_to_string(timestamp), user_id))

    return cursor.lastrowid
