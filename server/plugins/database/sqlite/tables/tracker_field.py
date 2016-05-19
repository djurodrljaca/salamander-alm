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

from plugins.database.sqlite.connection import ConnectionSqlite
from database.tables.tracker_field import TrackerFieldTable
import sqlite3
from typing import List, Optional


class TrackerFieldTableSqlite(TrackerFieldTable):
    """
    Implementation of "tracker_field" table for SQLite database

    Table's columns:

    - id:           int
    - tracker_id:   int, references tracker.id
    """

    def __init__(self):
        """
        Constructor
        """
        TrackerFieldTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE tracker_field (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    tracker_id  INTEGER REFERENCES tracker (id)\n"
            "                        NOT NULL\n"
            ")")

    def read_all_ids(self, connection: ConnectionSqlite, tracker_id: int) -> List[int]:
        """
        Reads IDs of all tracker fields in the database that belong to the specified tracker

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker

        :return:    List of tracker field IDs
        """
        cursor = connection.native_connection.execute(
            "SELECT id\n"
            "FROM tracker_field\n"
            "WHERE (tracker_id = :tracker_id)",
            {"tracker_id": tracker_id})

        trackers = list()

        for row in cursor.fetchall():
            trackers.append(row[0])

        return trackers

    def insert_row(self, connection: ConnectionSqlite, tracker_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO tracker_field\n"
                "   (id,\n"
                "    tracker_id)\n"
                "VALUES (NULL,\n"
                "        :tracker_id)",
                {"tracker_id": tracker_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
