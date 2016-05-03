import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "user_authentication"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE user_authentication (\n"
        "    id            INTEGER PRIMARY KEY AUTOINCREMENT\n"
        "                          NOT NULL,\n"
        "    user_id       INTEGER REFERENCES user (id) \n"
        "                          NOT NULL,\n"
        "    type          TEXT    NOT NULL,\n"
        "    revision_id   INTEGER REFERENCES revision (id) \n"
        "                          NOT NULL\n"
        ");")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user_authentication"

    :param connection: Connection to database
    """
    return


def insert_record(connection: sqlite3.Connection, user_id: int, type: str, revision_id: int) -> int:
    """
    Inserts a new record in the table: "user_authentication"

    :param connection: Connection to database
    :param user_id: ID of the user
    :param type: Authentication type
    :param revision_id: Revision for this record

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user_authentication\n"
        "   (id, user_id, type, revision_id)\n"
        "VALUES (NULL, ?, ?, ?);",
        (user_id, type, revision_id))

    return cursor.lastrowid


def find_authentication(connection: sqlite3.Connection, user_id: int, max_revision_id: int) -> dict:
    """
    Find authentication information for the specified user

    :param connection: Connection to database
    :param user_id: User ID
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: Authentication type
    """
    cursor = connection.execute(
        "SELECT id, type\n"
        "FROM user_authentication\n"
        "WHERE ((user_id = :user_id) AND\n"
        "       (revision_id =\n"
        "           (\n"
        "               SELECT MAX(revision_id)\n"
        "               FROM user_authentication\n"
        "               WHERE ((user_id = :user_id) AND\n"
        "                      (revision_id <= :max_revision_id))\n"
        "           )))",
        {"user_id": user_id, "max_revision_id": max_revision_id})

    # Process result
    record = cursor.fetchone()

    if record is not None:
        return dict(record)

    return None
