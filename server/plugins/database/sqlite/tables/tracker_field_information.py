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
from database.tables.tracker_field_information import \
    TrackerFieldInformationTable,\
    TrackerFieldSelection
import sqlite3
from typing import Any, List, Optional


class TrackerFieldInformationTableSqlite(TrackerFieldInformationTable):
    """
    Implementation of "tracker_field_information" table for SQLite database

    Table's columns:

    - id:               int
    - tracker_field_id: int, references tracker_field.id
    - name:             str
    - display_name:     str
    - description:      Optional[str]
    - field_type:       str
    - required:         bool
    - active:           bool
    - revision_id:      int, references revision.id
    """

# TODO: add "required" field

    def __init__(self):
        """
        Constructor
        """
        TrackerFieldInformationTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE tracker_field_information (\n"
            "    id                  INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                                NOT NULL,\n"
            "    tracker_field_id    INTEGER REFERENCES tracker_field (id)\n"
            "                                NOT NULL,\n"
            "    name                TEXT    NOT NULL\n"
            "                                CHECK (length(name) > 0),\n"
            "    display_name        TEXT    NOT NULL\n"
            "                                CHECK (length(display_name) > 0),\n"
            "    description         TEXT,\n"
            "    field_type          TEXT    NOT NULL\n"
            "                                CHECK (length(field_type) > 0),\n"
            "    required            BOOLEAN NOT NULL\n"
            "                                CHECK ( (required = 0) OR\n"
            "                                        (required = 1) ),\n"
            "    active              BOOLEAN NOT NULL\n"
            "                                CHECK ( (active = 0) OR\n"
            "                                        (active = 1) ),\n"
            "    revision_id         INTEGER REFERENCES revision (id) \n"
            "                                NOT NULL\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_field_information_ix_tracker_field_id\n"
            "ON tracker_field_information (\n"
            "    tracker_field_id\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_field_information_ix_name ON tracker_field_information (\n"
            "    name\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX tracker_field_information_ix_display_name\n"
            "ON tracker_field_information (\n"
            "    display_name\n"
            ")")

    def read_all_tracker_field_ids(self,
                                   connection: ConnectionSqlite,
                                   tracker_id: int,
                                   tracker_field_selection: TrackerFieldSelection,
                                   max_revision_id: int) -> List[int]:
        """
        Reads IDs of all tracker field IDs in the database that belong to the specified tracker

        :param connection:              Database connection
        :param tracker_id:              ID of the tracker
        :param tracker_field_selection: Search for active, inactive or all tracker fields
        :param max_revision_id:         Maximum revision ID for the search

        :return:    List of tracker field IDs
        """
        query = (
            "SELECT TFI.tracker_field_id\n"
            "FROM tracker_field as TF\n"
            "INNER JOIN (\n"
            "    SELECT TFI1.tracker_field_id,\n"
            "           TFI1.active\n"
            "    FROM tracker_field_information AS TFI1\n"
            "    WHERE (TFI1.revision_id = (\n"
            "                SELECT MAX(TFI2.revision_id)\n"
            "                FROM tracker_field_information AS TFI2\n"
            "                WHERE ((TFI2.tracker_field_id = TFI1.tracker_field_id) AND\n"
            "                       (TFI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ") AS TFI\n"
            "ON (TF.id = TFI.tracker_field_id)"
        )

        if tracker_field_selection == TrackerFieldSelection.Active:
            query += ("WHERE ((TF.tracker_id = :tracker_id) AND\n"
                      "       (TFI.active = 1))")
        elif tracker_field_selection == TrackerFieldSelection.Inactive:
            query += ("WHERE ((TF.tracker_id = :tracker_id) AND\n"
                      "       (TFI.active = 0))")
        else:
            query += "WHERE (TF.tracker_id = :tracker_id)"

        cursor = connection.native_connection.execute(query, {"tracker_id": tracker_id,
                                                              "max_revision_id": max_revision_id})

        # Process result
        tracker_fields = list()

        for row in cursor.fetchall():
            if row is not None:
                tracker_fields.append(row[0])

        return tracker_fields

    def read_information(self,
                         connection: ConnectionSqlite,
                         attribute_name: str,
                         attribute_value: Any,
                         tracker_field_selection: TrackerFieldSelection,
                         max_revision_id: int) -> List[dict]:
        """
        Reads tracker field information for the specified tracker field, state (active/inactive) and
        max revision

        :param connection:              Database connection
        :param attribute_name:          Search attribute name
        :param attribute_value:         Search attribute value
        :param tracker_field_selection: Search for active, inactive or all trackers
        :param max_revision_id:         Maximum revision ID for the search

        :return:    Tracker field information of all tracker fields that match the search attribute

        Only the following search attributes are supported:

        - tracker_field_id
        - name
        - display_name

        Each dictionary in the returned list contains items:

        - tracker_id
        - tracker_field_id
        - name
        - display_name
        - description
        - field_type
        - required
        - active
        - revision_id
        """
        if attribute_name not in ["tracker_field_id", "name", "display_name"]:
            raise AttributeError("Unsupported attribute name")

        # Read the users that match the search attribute
        query = (
            "SELECT TF.tracker_id,\n"
            "       TFI.tracker_field_id,\n"
            "       TFI.name,\n"
            "       TFI.display_name,\n"
            "       TFI.description,\n"
            "       TFI.field_type,\n"
            "       TFI.required,\n"
            "       TFI.active,\n"
            "       TFI.revision_id\n"
            "FROM tracker_field as TF\n"
            "INNER JOIN (\n"
            "    SELECT TFI1.tracker_field_id,\n"
            "           TFI1.name,\n"
            "           TFI1.display_name,\n"
            "           TFI1.description,\n"
            "           TFI1.field_type,\n"
            "           TFI1.required,\n"
            "           TFI1.active,\n"
            "           TFI1.revision_id\n"
            "    FROM tracker_field_information AS TFI1\n"
            "    WHERE (TFI1.revision_id = (\n"
            "                SELECT MAX(TFI2.revision_id)\n"
            "                FROM tracker_field_information AS TFI2\n"
            "                WHERE ((TFI2.tracker_field_id = TFI1.tracker_field_id) AND\n"
            "                       (TFI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ") AS TFI\n"
            "ON (TF.id = TFI.tracker_field_id)"
        )

        if tracker_field_selection == TrackerFieldSelection.Active:
            query += ("WHERE ((TFI.{0} = :attribute_value) AND\n"
                      "       (TFI.active = 1))")
        elif tracker_field_selection == TrackerFieldSelection.Inactive:
            query += ("WHERE ((TFI.{0} = :attribute_value) AND\n"
                      "       (TFI.active = 0))")
        else:
            query += "WHERE (TFI.{0} = :attribute_value)"

        cursor = connection.native_connection.execute(query.format(attribute_name),
                                                      {"attribute_value": attribute_value,
                                                       "max_revision_id": max_revision_id})

        # Process result
        tracker_fields = list()

        for row in cursor.fetchall():
            if row is not None:
                tracker_field = {"tracker_id": row["TF.tracker_id"],
                                 "tracker_field_id": row["TFI.tracker_field_id"],
                                 "name": row["TFI.name"],
                                 "display_name": row["TFI.display_name"],
                                 "description": row["TFI.description"],
                                 "field_type": row["TFI.field_type"],
                                 "required": bool(row["TFI.required"]),
                                 "active": bool(row["TFI.active"]),
                                 "revision_id": row["TFI.revision_id"]}
                tracker_fields.append(tracker_field)

        return tracker_fields

    def insert_row(self,
                   connection: ConnectionSqlite,
                   tracker_field_id: int,
                   name: str,
                   display_name: str,
                   description: str,
                   field_type: str,
                   required: bool,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:          Database connection
        :param tracker_field_id:    ID of the tracker field
        :param name:                Tracker field name
        :param display_name:        Tracker field display name
        :param description:         Tracker field description
        :param field_type:          Tracker field type
        :param required:            Necessity of the tracker field (required or not)
        :param active:              State of the tracker field (active or inactive)
        :param revision_id:         Revision ID

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO tracker_field_information\n"
                "   (id,\n"
                "    tracker_field_id,\n"
                "    name,\n"
                "    display_name,\n"
                "    description,\n"
                "    field_type,\n"
                "    required,\n"
                "    active,\n"
                "    revision_id)\n"
                "VALUES (NULL,\n"
                "        :tracker_field_id,\n"
                "        :name,\n"
                "        :display_name,\n"
                "        :description,\n"
                "        :field_type,\n"
                "        :required,\n"
                "        :active,\n"
                "        :revision_id)",
                {"tracker_field_id": tracker_field_id,
                 "name": name,
                 "display_name": display_name,
                 "description": description,
                 "field_type": field_type,
                 "required": required,
                 "active": active,
                 "revision_id": revision_id})

            row_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Error occurred
            row_id = None

        return row_id
