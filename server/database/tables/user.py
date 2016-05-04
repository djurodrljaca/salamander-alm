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
