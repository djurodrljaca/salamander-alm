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
from database.tables.artifact_information import ArtifactInformationTable, ArtifactSelection
import sqlite3
from typing import Any, List, Optional


class ArtifactInformationTableSqlite(ArtifactInformationTable):
    """
    Implementation of "artifact_information" table for SQLite database

    Table's columns:

    - id:           int
    - artifact_id:  int, references artifact.id
    - locked:       bool
    - active:       bool
    - revision_id:  int, references revision.id
    """

# TODO: add "required" field

    def __init__(self):
        """
        Constructor
        """
        ArtifactInformationTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE artifact_information (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    artifact_id INTEGER REFERENCES artifact (id)\n"
            "                        NOT NULL,\n"
            "    locked      BOOLEAN NOT NULL\n"
            "                        CHECK ( (locked = 0) OR\n"
            "                                (locked = 1) ),\n"
            "    active      BOOLEAN NOT NULL\n"
            "                        CHECK ( (active = 0) OR\n"
            "                                (active = 1) ),\n"
            "    revision_id INTEGER REFERENCES revision (id) \n"
            "                        NOT NULL\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX artifact_information_ix_artifact_id\n"
            "ON artifact_information (\n"
            "    artifact_id\n"
            ")")

    def read_all_artifact_ids(self,
                              connection: ConnectionSqlite,
                              tracker_id: int,
                              artifact_selection: ArtifactSelection,
                              max_revision_id: int) -> List[int]:
        """
        Reads IDs of all artifact in the database that belong to the specified tracker

        :param connection:          Database connection
        :param tracker_id:          ID of the tracker
        :param artifact_selection:  Search for active, inactive or all artifacts
        :param max_revision_id:     Maximum revision ID for the search

        :return:    List of artifact IDs
        """
        query = (
            "SELECT AI.artifact_id\n"
            "FROM artifact as A\n"
            "INNER JOIN (\n"
            "    SELECT AI1.artifact_id,\n"
            "           AI1.active\n"
            "    FROM artifact_information AS AI1\n"
            "    WHERE (AI1.revision_id = (\n"
            "                SELECT MAX(AI2.revision_id)\n"
            "                FROM artifact_information AS AI2\n"
            "                WHERE ((AI2.artifact_id = AI1.artifact_id) AND\n"
            "                       (AI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ") AS AI\n"
            "ON (A.id = AI.artifact_id)"
        )

        if artifact_selection == ArtifactSelection.Active:
            query += ("WHERE ((A.tracker_id = :tracker_id) AND\n"
                      "       (AI.active = 1))")
        elif artifact_selection == ArtifactSelection.Inactive:
            query += ("WHERE ((A.tracker_id = :tracker_id) AND\n"
                      "       (AI.active = 0))")
        else:
            query += "WHERE (A.tracker_id = :tracker_id)"

        cursor = connection.native_connection.execute(query, {"tracker_id": tracker_id,
                                                              "max_revision_id": max_revision_id})

        # Process result
        artifacts = list()

        for row in cursor.fetchall():
            if row is not None:
                artifacts.append(row[0])

        return artifacts

    def read_information(self,
                         connection: ConnectionSqlite,
                         artifact_id: int,
                         max_revision_id: int) -> Optional[dict]:
        """
        Reads artifact information for the specified artifact and max revision

        :param connection:      Database connection
        :param artifact_id:     Artifact ID
        :param max_revision_id: Maximum revision ID for the search

        :return:    Artifact information

        Returned dictionary contains items:

        - id
        - artifact_id
        - locked
        - active
        - revision_id
        """
        # Read the users that match the search attribute
        cursor = connection.native_connection.execute(
            "SELECT AI1.id,\n"
            "       AI1.artifact_id,\n"
            "       AI1.locked,\n"
            "       AI1.active,\n"
            "       AI1.revision_id\n"
            "FROM artifact_information AS AI1\n"
            "WHERE ((AI1.artifact_id = :artifact_id) AND\n"
            "       (AI1.revision_id <= :max_revision_id))\n",
            {"artifact_id": artifact_id,
             "max_revision_id": max_revision_id})

        # Process result
        artifact = None
        row = cursor.fetchone()

        if row is not None:
            artifact = {"id": row["id"],
                        "artifact_id": row["artifact_id"],
                        "locked": bool(row["locked"]),
                        "active": bool(row["active"]),
                        "revision_id": row["revision_id"]}

        return artifact

    def insert_row(self,
                   connection: ConnectionSqlite,
                   artifact_id: int,
                   locked: bool,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param artifact_id: Artifact ID
        :param locked:      Lock state of the artifact (locked or unlocked)
        :param active:      State of the artifact (active or inactive)
        :param revision_id: Revision ID

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO artifact_information\n"
                "   (id,\n"
                "    artifact_id,\n"
                "    locked,\n"
                "    active,\n"
                "    revision_id)\n"
                "VALUES (NULL,\n"
                "        :artifact_id,\n"
                "        :locked,\n"
                "        :active,\n"
                "        :revision_id)",
                {"artifact_id": artifact_id,
                 "locked": locked,
                 "active": active,
                 "revision_id": revision_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
