"""
Salamander ALM
Copyright (c) 2016  Djuro Drljaca

This Python module is free software; you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This Python module is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library. If
not, see <http://www.gnu.org/licenses/>.
"""

import sqlite3
from typing import Optional


# --------------------------------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------------------------------


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
        ")")


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
        "VALUES (NULL, ?, ?, ?)",
        (user_authentication_id, password_hash, revision_id))

    return cursor.lastrowid


def find_password_hash(connection: sqlite3.Connection,
                       user_authentication_id: int,
                       max_revision_id: int) -> Optional[str]:
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
        "       (revision_id = (\n"
        "           SELECT MAX(revision_id)"
        "           FROM user_authentication_basic\n"
        "           WHERE ((user_authentication_id = :user_authentication_id) AND\n"
        "                  (revision_id <= :max_revision_id))\n"
        "        )))",
        {"user_authentication_id": user_authentication_id, "max_revision_id": max_revision_id})

    # Process result
    record = cursor.fetchone()

    if record is not None:
        return record[0]

    return None
