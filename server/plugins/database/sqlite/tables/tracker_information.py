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
from database.tables.tracker_information import TrackerInformationTable, TrackerSelection
import sqlite3
from typing import Any, List, Optional


class TrackerInformationTableSqlite(TrackerInformationTable):
    """
    Implementation of "tracker_information" table for SQLite database

    Table's columns:

    - id:           int
    - tracker_id:   int, references tracker.id
    - short_name:   str
    - full_name:    str
    - description:  Optional[str]
    - active:       bool
    - revision_id:  int, references revision.id
    """

    def __init__(self):
        """
        Constructor
        """
        TrackerInformationTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE tracker_information (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    tracker_id  INTEGER REFERENCES tracker (id)\n"
            "                        NOT NULL,\n"
            "    short_name  TEXT    NOT NULL\n"
            "                        CHECK (length(short_name) > 0),\n"
            "    full_name   TEXT    NOT NULL\n"
            "                        CHECK (length(full_name) > 0),\n"
            "    description TEXT,\n"
            "    active      BOOLEAN NOT NULL\n"
            "                        CHECK ( (active = 0) OR\n"
            "                                (active = 1) ),\n"
            "    revision_id INTEGER REFERENCES revision (id) \n"
            "                        NOT NULL\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_information_ix_tracker_id ON tracker_information (\n"
            "    tracker_id\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_information_ix_short_name ON tracker_information (\n"
            "    short_name\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_information_ix_full_name ON tracker_information (\n"
            "    full_name\n"
            ")")

    def read_all_tracker_ids(self,
                             connection: ConnectionSqlite,
                             project_id: int,
                             tracker_selection: TrackerSelection,
                             max_revision_id: int) -> List[int]:
        """
        Reads IDs of all tracker IDs in the database that belong to the specified project

        :param connection:          Database connection
        :param project_id:          ID of the project
        :param tracker_selection:   Search for active, inactive or all trackers
        :param max_revision_id:     Maximum revision ID for the search

        :return:    List of tracker IDs
        """
        query = (
            "SELECT TI.tracker_id\n"
            "FROM tracker as T\n"
            "INNER JOIN (\n"
            "    SELECT TI1.tracker_id,\n"
            "           TI1.active\n"
            "    FROM tracker_information AS TI1\n"
            "    WHERE (TI1.revision_id = (\n"
            "                SELECT MAX(TI2.revision_id)\n"
            "                FROM tracker_information AS TI2\n"
            "                WHERE ((TI2.tracker_id = TI1.tracker_id) AND\n"
            "                       (TI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ") AS TI\n"
            "ON (T.id = TI.tracker_id)"
        )

        if tracker_selection == TrackerSelection.Active:
            query += ("WHERE ((T.project_id = :project_id) AND\n"
                      "       (TI.active = 1))")
        elif tracker_selection == TrackerSelection.Inactive:
            query += ("WHERE ((T.project_id = :project_id) AND\n"
                      "       (TI.active = 0))")
        else:
            query += "WHERE (T.project_id = :project_id)"

        cursor = connection.native_connection.execute(query, {"project_id": project_id,
                                                              "max_revision_id": max_revision_id})

        # Process result
        trackers = list()

        for row in cursor.fetchall():
            if row is not None:
                trackers.append(row["TI.tracker_id"])

        return trackers

    def read_information(self,
                         connection: ConnectionSqlite,
                         attribute_name: str,
                         attribute_value: Any,
                         tracker_selection: TrackerSelection,
                         max_revision_id: int) -> List[dict]:
        """
        Reads tracker information for the specified tracker, state (active/inactive) and max
        revision

        :param connection:          Database connection
        :param attribute_name:      Search attribute name
        :param attribute_value:     Search attribute value
        :param tracker_selection:   Search for active, inactive or all trackers
        :param max_revision_id:     Maximum revision ID for the search

        :return:    Tracker information of all trackers that match the search attribute

        Only the following search attributes are supported:

        - tracker_id
        - short_name
        - full_name

        Each dictionary in the returned list contains items:

        - project_id
        - tracker_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        if attribute_name not in ["tracker_id", "short_name", "full_name"]:
            raise AttributeError("Unsupported attribute name")

        # Read the users that match the search attribute
        query = (
            "SELECT T.project_id,\n"
            "       TI.tracker_id,\n"
            "       TI.short_name,\n"
            "       TI.full_name,\n"
            "       TI.description,\n"
            "       TI.active,\n"
            "       TI.revision_id\n"
            "FROM tracker as T\n"
            "INNER JOIN (\n"
            "    SELECT TI1.tracker_id,\n"
            "           TI1.short_name,\n"
            "           TI1.full_name,\n"
            "           TI1.description,\n"
            "           TI1.active,\n"
            "           TI1.revision_id\n"
            "    FROM tracker_information AS TI1\n"
            "    WHERE (TI1.revision_id = (\n"
            "                SELECT MAX(TI2.revision_id)\n"
            "                FROM tracker_information AS TI2\n"
            "                WHERE ((TI2.tracker_id = TI1.tracker_id) AND\n"
            "                       (TI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ") AS TI\n"
            "ON (T.id = TI.tracker_id)"
        )

        if tracker_selection == TrackerSelection.Active:
            query += ("WHERE ((TI.{0} = :attribute_value) AND\n"
                      "       (TI.active = 1))")
        elif tracker_selection == TrackerSelection.Inactive:
            query += ("WHERE ((TI.{0} = :attribute_value) AND\n"
                      "       (TI.active = 0))")
        else:
            query += "WHERE (TI.{0} = :attribute_value)"

        cursor = connection.native_connection.execute(query.format(attribute_name),
                                                      {"attribute_value": attribute_value,
                                                       "max_revision_id": max_revision_id})

        # Process result
        trackers = list()

        for row in cursor.fetchall():
            if row is not None:
                tracker = {"project_id": row["T.project_id"],
                           "tracker_id": row["TI.tracker_id"],
                           "short_name": row["TI.short_name"],
                           "full_name": row["TI.full_name"],
                           "description": row["TI.description"],
                           "active": bool(row["TI.active"]),
                           "revision_id": row["TI.revision_id"]}
                trackers.append(tracker)

        return trackers

    def insert_row(self,
                   connection: ConnectionSqlite,
                   tracker_id: int,
                   short_name: str,
                   full_name: str,
                   description: str,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker
        :param short_name:  Tracker short name
        :param full_name:   Tracker full name
        :param description: Tracker description
        :param active:      State of the tracker (active or inactive)
        :param revision_id: Revision ID

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO tracker_information\n"
                "   (id,\n"
                "    tracker_id,\n"
                "    short_name,\n"
                "    full_name,\n"
                "    description,\n"
                "    active,\n"
                "    revision_id)\n"
                "VALUES (NULL,\n"
                "        :tracker_id,\n"
                "        :short_name,\n"
                "        :full_name,\n"
                "        :description,\n"
                "        :active,\n"
                "        :revision_id)",
                {"tracker_id": tracker_id,
                 "short_name": short_name,
                 "full_name": full_name,
                 "description": description,
                 "active": active,
                 "revision_id": revision_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
