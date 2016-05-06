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
from database.tables.revision import RevisionTable
from database.datatypes import datetime_from_string, datetime_to_string
import datetime
from typing import List, Optional


class RevisionTableSqlite(RevisionTable):
    """
    Implementation of "revision" table for SQLite database
    """

    def __init__(self):
        """
        Constructor
        """
        RevisionTable.__init__(self)

    def __del__(self):
        """
        Destructor
        """
        RevisionTable.__del__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE revision (\n"
            "    id        INTEGER  PRIMARY KEY AUTOINCREMENT\n"
            "                       NOT NULL,\n"
            "    timestamp DATETIME,\n"
            "    user_id   INTEGER  REFERENCES user (id)\n"
            "                       NOT NULL\n"
            ")")

    def read_current_revision_id(self, connection: ConnectionSqlite) -> Optional[int]:
        """
        Reads the current revision ID from the database

        :param connection:  Database connection

        :return:    ID of the current revision
        """
        cursor = connection.native_connection.execute("SELECT MAX(id) FROM revision")
        row = cursor.fetchone()

        revision_id = None

        if row is not None:
            revision_id = row[0]

        return revision_id

    def read_revision(self, connection: ConnectionSqlite, revision_id: int) -> Optional[dict]:
        """
        Reads the revision information from the database

        :param connection:  Database connection
        :param revision_id: ID of the revision to read

        :return:    Revision information
        """
        cursor = connection.native_connection.execute(
            "SELECT id,\n"
            "       timestamp,\n"
            "       user_id\n"
            "FROM revision\n"
            "WHERE (id = :id)",
            {"id": revision_id})

        revision = None
        row = cursor.fetchone()

        if row is not None:
            revision = {"id": row["id"],
                        "timestamp": datetime_from_string(row["timestamp"]),
                        "user_id": row["user_id"]}

        return revision

    def read_revisions_by_id_range(self,
                                   connection: ConnectionSqlite,
                                   min_revision_id: int,
                                   max_revision_id: int) -> List[dict]:
        """
        Reads the revision information from the database

        :param connection:      Database connection
        :param min_revision_id: Smallest revision ID to be included
        :param max_revision_id: Biggest revision ID to be included

        :return:    Revision
        """
        revisions = list()

        if min_revision_id <= max_revision_id:
            cursor = connection.native_connection.execute(
                "SELECT id,\n"
                "       timestamp,\n"
                "       user_id\n"
                "FROM revision\n"
                "WHERE (id >= :min_revision_id) AND"
                "      (id <= :max_revision_id)",
                {"min_revision_id": min_revision_id,
                 "max_revision_id": max_revision_id})

            for row in cursor.fetchall():
                revision = {"id": row["id"],
                            "timestamp": datetime_from_string(row["timestamp"]),
                            "user_id": row["user_id"]}
                revisions.append(revision)

        return revisions

    def read_revisions_by_time_range(self,
                                     connection: ConnectionSqlite,
                                     min_timestamp: datetime.datetime,
                                     max_timestamp: datetime.datetime) -> List[dict]:
        """
        Reads the revision information from the database

        :param connection:      Database connection
        :param min_timestamp:   Earliest timestamp to be included
        :param max_timestamp:   Latest timestamp to be included

        :return:    List of revisions
        """
        revisions = list()

        if min_timestamp <= max_timestamp:
            cursor = connection.native_connection.execute(
                "SELECT id,\n"
                "       timestamp,\n"
                "       user_id\n"
                "FROM revision\n"
                "WHERE (timestamp >= :min_timestamp) AND"
                "      (timestamp <= :max_timestamp)",
                {"min_timestamp": min_timestamp,
                 "max_revision_id": max_timestamp})

            for row in cursor.fetchall():
                revision = {"id": row["id"],
                            "timestamp": datetime_from_string(row["timestamp"]),
                            "user_id": row["user_id"]}
                revisions.append(revision)

        return revisions

    def insert_row(self,
                   connection: ConnectionSqlite,
                   timestamp: datetime.datetime,
                   user_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param timestamp:   Timestamp
        :param user_id:     ID of the user

        :return: ID of the newly created row
        """
        cursor = connection.native_connection.execute(
            "INSERT INTO revision\n"
            "   (id, timestamp, user_id)\n"
            "VALUES (NULL, :timestamp, :user_id)",
            {"timestamp": datetime_to_string(timestamp),
             "user_id": user_id})

        return cursor.lastrowid
