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
from database.datatypes import datetime_from_string, datetime_to_string
from database.tables.artifact import ArtifactTable
import datetime
import sqlite3
from typing import List, Optional


class ArtifactTableSqlite(ArtifactTable):
    """
    Implementation of "artifact" table for SQLite database

    Table's columns:

    - id:           int
    - tracker_id:   int, references tracker.id
    - created_on:   datetime
    - created_by:   int, references user.id
    """

    def __init__(self):
        """
        Constructor
        """
        ArtifactTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE artifact (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    tracker_id  INTEGER REFERENCES tracker (id)\n"
            "                        NOT NULL,\n"
            "    created_on  TEXT    NOT NULL\n"
            "                        CHECK (length(created_on) >= 23),\n"
            "    created_by  INTEGER REFERENCES user (id)\n"
            "                        NOT NULL\n"
            ")")

    def read_all_ids(self, connection: ConnectionSqlite, tracker_id: int) -> List[int]:
        """
        Reads IDs of all artifacts in the database that belong to the specified tracker

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker

        :return:    List of artifact IDs
        """
        cursor = connection.native_connection.execute(
            "SELECT id\n"
            "FROM artifact\n"
            "WHERE (tracker_id = :tracker_id)",
            {"tracker_id": tracker_id})

        artifacts = list()

        for row in cursor.fetchall():
            artifacts.append(row[0])

        return artifacts

    def read_artifact(self, connection: ConnectionSqlite, artifact_id: int) -> Optional[dict]:
        """
        Reads the artifact information from the database

        :param connection:  Database connection
        :param artifact_id: ID of the artifact

        :return:    Artifact information

        Returned dictionary contains items:

        - id
        - tracker_id
        - created_on
        - created_by
        """
        cursor = connection.native_connection.execute(
            "SELECT id,\n"
            "       tracker_id,\n"
            "       created_on,\n"
            "       created_by\n"
            "FROM revision\n"
            "WHERE (id = :id)",
            {"id": artifact_id})

        artifact = None
        row = cursor.fetchone()

        if row is not None:
            artifact = {"id": row["id"],
                        "tracker_id": row["tracker_id"],
                        "created_on": datetime_from_string(row["created_on"]),
                        "created_by": row["created_by"]}

        return artifact


    def insert_row(self,
                   connection: ConnectionSqlite,
                   tracker_id: int,
                   created_on: datetime.datetime,
                   created_by: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker
        :param created_on:  Timestamp when artifact was created
        :param created_by:  ID of the user that created the artifact

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO artifact\n"
                "   (id,\n"
                "    tracker_id,\n"
                "    created_on,\n"
                "    created_by)\n"
                "VALUES (NULL,\n"
                "        :tracker_id,\n"
                "        :created_on,\n"
                "        :created_by)",
                {"tracker_id": tracker_id,
                 "created_on": datetime_to_string(created_on),
                 "created_by": created_by})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
