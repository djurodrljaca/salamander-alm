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
from typing import Any, List, Optional


# --------------------------------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------------------------------


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
        "    active                BOOLEAN NOT NULL,\n"
        "    revision_id           INTEGER REFERENCES revision (id) \n"
        "                                  NOT NULL\n"
        ")")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create indexes for table: "user_information"

    :param connection: Connection to database
    """
    connection.execute(
        "CREATE INDEX user_information_ix_user_name ON user_information (\n"
        "    user_name\n"
        ")")

    connection.execute(
        "CREATE INDEX user_information_ix_display_name ON user_information (\n"
        "    display_name\n"
        ")")


def find_users_by_attribute(connection: sqlite3.Connection,
                            attribute_name: str,
                            attribute_value: Any,
                            max_revision_id: int) -> List[dict]:
    """
    Find users that match the specified search attribute

    :param connection: Connection to database
    :param attribute_name: Search attribute name
    :param attribute_value: Search attribute value
    :param max_revision_id: Maximum allowed revision ID for the search

    :return: Users that match the search attribute

    Only the following search attributes are supported:
    - user_id
    - user_name
    - display_name
    - email
    """
    # Find the users that match the search attribute
    query = (
        "SELECT user_id,\n"
        "       user_name,\n"
        "       display_name,\n"
        "       email,\n"
        "       revision_id\n"
        "FROM (\n"
        "    SELECT UI1.user_id,\n"
        "           UI1.user_name,\n"
        "           UI1.display_name,\n"
        "           UI1.email,\n"
        "           UI1.active,\n"
        "           UI1.revision_id\n"
        "    FROM user_information AS UI1\n"
        "    WHERE (UI1.revision_id = (\n"
        "                SELECT MAX(UI2.revision_id)\n"
        "                FROM user_information AS UI2\n"
        "                WHERE ((UI2.user_id = UI1.user_id) AND\n"
        "                       (UI2.revision_id <= :max_revision_id))\n"
        "           ))\n"
        ")\n"
        "WHERE (({0} = :attribute_value) AND\n"
        "       (active = 1))"
    ).format(attribute_name)

    cursor = connection.execute(query, {"attribute_value": attribute_value,
                                        "max_revision_id": max_revision_id})

    # Process result
    users = list()

    for record in cursor.fetchall():
        if record is not None:
            user = dict(record)
            users.append(user)

    return users


def insert_record(connection: sqlite3.Connection,
                  user_id: int,
                  user_name: str,
                  display_name: str,
                  email: str,
                  active: bool,
                  revision_id: int) -> Optional[int]:
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

    :return: ID of the inserted record
    """
    cursor = connection.execute(
        "INSERT INTO user_information\n"
        "   (id, user_id, user_name, display_name, email, active, revision_id)\n"
        "VALUES (NULL, ?, ?, ?, ?, ?, ?)",
        (user_id, user_name, display_name, email, active, revision_id))

    return cursor.lastrowid
