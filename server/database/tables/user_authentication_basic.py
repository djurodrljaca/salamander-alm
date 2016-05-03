import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "user_authentication_basic"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE user_authentication_basic (\n"
        "    id                     INTEGER PRIMARY KEY AUTOINCREMENT\n"
        "                                   NOT NULL,\n"
        "    user_authentication_id INTEGER REFERENCES user (id) \n"
        "                                   NOT NULL,\n"
        "    password_hash          TEXT    NOT NULL,\n"
        "    revision_id            INTEGER REFERENCES revision (id) \n"
        "                                   NOT NULL\n"
        ");")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user"

    :param connection: Connection to database
    """
    return


def insert_record(connection: sqlite3.Connection,
                  user_authentication_id: int,
                  password_hash: str,
                  revision_id: int) -> int:
    """
    Inserts a new record in the table: "user_authentication_basic"

    :param connection: Connection to database
    :param user_authentication_id: ID of the user authentication record
    :param password_hash: Hash of the user's password
    :param revision_id: Revision for this record

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user_authentication_basic"
        "   (id, user_authentication_id, password_hash, revision_id)\n"
        "VALUES (NULL, ?, ?, ?);",
        (user_authentication_id, password_hash, revision_id))

    return cursor.lastrowid


def find_password_hash(connection: sqlite3.Connection,
                       user_authentication_id: int,
                       max_revision_id: int) -> str:
    """
    Find password hash for the specified user

    :param connection: Connection to database
    :param user_authentication_id: ID of the user authentication record
    :param max_revision_id: Maximum allowed revision ID for the search
    :return:
    """
    cursor = connection.execute(
        "SELECT password_hash\n"
        "FROM user_authentication_basic\n"
        "WHERE ((user_authentication_id = :user_authentication_id) AND\n"
        "       (revision_id = \n"
        "           (\n"
        "               SELECT MAX(revision_id)"
        "               FROM user_authentication_basic\n"
        "               WHERE ((user_authentication_id = :user_authentication_id) AND\n"
        "                      (revision_id <= :max_revision_id))\n"
        "           )));",
        {"user_authentication_id": user_authentication_id, "max_revision_id": max_revision_id})

    # Process result
    record = cursor.fetchone()

    if record is not None:
        return record[0]

    return None
