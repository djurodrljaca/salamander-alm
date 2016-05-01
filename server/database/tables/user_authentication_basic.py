import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "user_authentication_basic"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE user_authentication_basic (\n"
        "    id            INTEGER PRIMARY KEY AUTOINCREMENT\n"
        "                          NOT NULL,\n"
        "    user_id       INTEGER REFERENCES user (id) \n"
        "                          NOT NULL,\n"
        "    password_hash TEXT    NOT NULL,\n"
        "    revision_id   INTEGER REFERENCES revision (id) \n"
        "                          NOT NULL\n"
        ");")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user"

    :param connection: Connection to database
    """
    return


def insert_record(connection: sqlite3.Connection,
                  user_id: int,
                  password_hash: str,
                  revision_id: int) -> int:
    """
    Inserts a new record in the table: "user_authentication_basic"

    :param connection: Connection to database
    :param user_id: ID of the user
    :param password_hash: Hash of the user's password
    :param revision_id: Revision for this record

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user_authentication_basic (id, user_id, password_hash, revision_id)\n"
        "VALUES (NULL, ?, ?, ?);",
        (user_id, password_hash, revision_id))

    return cursor.lastrowid
