import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """
    Create table: "user_information"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE TABLE user_information (\n"
        "    id                    INTEGER PRIMARY KEY AUTOINCREMENT\n"
        "                                  NOT NULL,\n"
        "    user_id               INTEGER REFERENCES user (id) \n"
        "                                  NOT NULL,\n"
        "    user_name             TEXT    NOT NULL,\n"
        "    display_name          TEXT    NOT NULL,\n"
        "    email                 TEXT,\n"
        "    authentication_method TEXT    NOT NULL,\n"
        "    active                BOOLEAN NOT NULL,\n"
        "    revision_id           INTEGER REFERENCES revision (id) \n"
        "                                  NOT NULL\n"
        ");\n")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user_information"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE INDEX user_information_ix_user_name ON user_information (\n"
        "    user_name\n"
        ");")


def insert_record(connection: sqlite3.Connection,
                  user_id: int,
                  user_name: str,
                  display_name: str,
                  email: str,
                  authentication_method: str,
                  active: bool,
                  revision_id: int) -> int:
    """
    Inserts a new record in the table: "user_information"

    :param connection: Connection to database
    :param user_id: ID of the user
    :param user_name: User name
    :param display_name: User's name in format appropriate for displaying in the GUI
    :param email: Email address of the user
    :param authentication_method: Authentication method (for example: "basic")
    :param active: State of the user (active or inactive)
    :param revision_id: Revision for this record

    :return: 'id' of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user_information (id, user_id, user_name, display_name, email,\n"
        "                              authentication_method, active, revision_id)\n"
        "VALUES (NULL, ?, ?, ?, ?, ?, ?, ?);",
        (user_id, user_name, display_name, email, authentication_method, active, revision_id))

    return cursor.lastrowid
