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
from database.tables.tracker import TrackerTable
import sqlite3
from typing import List, Optional


class TrackerTableSqlite(TrackerTable):
    """
    Implementation of "tracker" table for SQLite database

    Table's columns:

    - id:           int
    - project_id:   int, references project.id
    """

    def __init__(self):
        """
        Constructor
        """
        TrackerTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE tracker (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    project_id  INTEGER REFERENCES project (id)\n"
            "                        NOT NULL\n"
            ")")

    def read_all_ids(self, connection: ConnectionSqlite, project_id: int) -> List[int]:
        """
        Reads IDs of all tracker IDs in the database that belong to the specified project

        :param connection:  Database connection
        :param project_id:  ID of the project

        :return:    List of tracker IDs
        """
        cursor = connection.native_connection.execute(
            "SELECT id\n"
            "FROM tracker\n"
            "WHERE (project_id = :project_id)",
            {"project_id": project_id})

        trackers = list()

        for row in cursor.fetchall():
            trackers.append(row[0])

        return trackers

    def insert_row(self, connection: ConnectionSqlite, project_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param project_id:  ID of the project

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO tracker\n"
                "   (id,"
                "    project_id)\n"
                "VALUES (NULL,"
                "        :project_id)",
                {"project_id": project_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
