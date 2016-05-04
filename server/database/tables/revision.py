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
