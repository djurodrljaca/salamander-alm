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
from database.tables.project_information import ProjectInformationTable, ProjectSelection
import sqlite3
from typing import Any, List, Optional


class ProjectInformationTableSqlite(ProjectInformationTable):
    """
    Implementation of "project_information" table for SQLite database

    Table's columns:

    - id:           int
    - project_id:   int, references project.id
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
        ProjectInformationTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE project_information (\n"
            "    id          INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "                        NOT NULL,\n"
            "    project_id  INTEGER REFERENCES project (id)\n"
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
            "CREATE INDEX project_information_ix_project_id ON project_information (\n"
            "    project_id\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX project_information_ix_short_name ON project_information (\n"
            "    short_name\n"
            ")")

        connection.native_connection.execute(
            "CREATE INDEX project_information_ix_full_name ON project_information (\n"
            "    full_name\n"
            ")")

    def read_all_project_ids(self,
                             connection: ConnectionSqlite,
                             project_selection: ProjectSelection,
                             max_revision_id: int) -> List[int]:
        """
        Reads IDs of all project IDs in the database

        :param connection:          Database connection
        :param project_selection:   Search for active, inactive or all projects
        :param max_revision_id:     Maximum revision ID for the search

        :return:    List of project IDs
        """
        query = (
            "SELECT project_id,\n"
            "       active\n"
            "FROM (\n"
            "    SELECT PI1.project_id,\n"
            "           PI1.short_name,\n"
            "           PI1.full_name,\n"
            "           PI1.description,\n"
            "           PI1.active,\n"
            "           PI1.revision_id\n"
            "    FROM project_information AS PI1\n"
            "    WHERE (PI1.revision_id = (\n"
            "                SELECT MAX(PI2.revision_id)\n"
            "                FROM project_information AS PI2\n"
            "                WHERE ((PI2.project_id = PI1.project_id) AND\n"
            "                       (PI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ")\n"
        )

        if project_selection == ProjectSelection.Active:
            query += "WHERE (active = 1)"
        if project_selection == ProjectSelection.Inactive:
            query += "WHERE (active = 0)"
        else:
            # Nothing needed for selecting all users
            pass

        cursor = connection.native_connection.execute(query, {"max_revision_id": max_revision_id})

        # Process result
        projects = list()

        for row in cursor.fetchall():
            if row is not None:
                projects.append(row["project_id"])

        return projects

    def read_information(self,
                         connection: ConnectionSqlite,
                         attribute_name: str,
                         attribute_value: Any,
                         project_selection: ProjectSelection,
                         max_revision_id: int) -> List[dict]:
        """
        Reads project information for the specified project, state (active/inactive) and max
        revision

        :param connection:          Database connection
        :param attribute_name:      Search attribute name
        :param attribute_value:     Search attribute value
        :param project_selection:   Search for active, inactive or all projects
        :param max_revision_id:     Maximum revision ID for the search

        :return:    Project information of all projects that match the search attribute

        Only the following search attributes are supported:

        - project_id
        - short_name
        - full_name

        Each dictionary in the returned list contains items:

        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        if attribute_name not in ["project_id", "short_name", "full_name"]:
            raise AttributeError("Unsupported attribute name")

        # Read the users that match the search attribute
        query = (
            "SELECT project_id,\n"
            "       short_name,\n"
            "       full_name,\n"
            "       description,\n"
            "       active,\n"
            "       revision_id\n"
            "FROM (\n"
            "    SELECT PI1.id,\n"
            "           PI1.project_id,\n"
            "           PI1.short_name,\n"
            "           PI1.full_name,\n"
            "           PI1.description,\n"
            "           PI1.active,\n"
            "           PI1.revision_id\n"
            "    FROM project_information AS PI1\n"
            "    WHERE (PI1.revision_id = (\n"
            "                SELECT MAX(PI2.revision_id)\n"
            "                FROM project_information AS PI2\n"
            "                WHERE ((PI2.project_id = PI1.project_id) AND\n"
            "                       (PI2.revision_id <= :max_revision_id))\n"
            "           ))\n"
            ")\n"
        )

        if project_selection == ProjectSelection.Active:
            query += ("WHERE (({0} = :attribute_value) AND\n"
                      "       (active = 1))")
        elif project_selection == ProjectSelection.Inactive:
            query += ("WHERE (({0} = :attribute_value) AND\n"
                      "       (active = 0))")
        else:
            query += "WHERE ({0} = :attribute_value)"

        cursor = connection.native_connection.execute(query.format(attribute_name),
                                                      {"attribute_value": attribute_value,
                                                       "max_revision_id": max_revision_id})

        # Process result
        projects = list()

        for row in cursor.fetchall():
            if row is not None:
                project = {"project_id": row["project_id"],
                           "short_name": row["short_name"],
                           "full_name": row["full_name"],
                           "description": row["description"],
                           "active": bool(row["active"]),
                           "revision_id": row["revision_id"]}
                projects.append(project)

        return projects

    def insert_row(self,
                   connection: ConnectionSqlite,
                   project_id: int,
                   short_name: str,
                   full_name: str,
                   description: str,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param project_id:  ID of the project
        :param short_name:  Project short name
        :param full_name:   Project full name
        :param description: Project description
        :param active:      State of the project (active or inactive)
        :param revision_id: Revision ID

        :return:    ID of the newly created row
        """
        try:
            cursor = connection.native_connection.execute(
                "INSERT INTO project_information\n"
                "   (id,\n"
                "    project_id,\n"
                "    short_name,\n"
                "    full_name,\n"
                "    description,\n"
                "    active,\n"
                "    revision_id)\n"
                "VALUES (NULL,\n"
                "        :project_id,\n"
                "        :short_name,\n"
                "        :full_name,\n"
                "        :description,\n"
                "        :active,\n"
                "        :revision_id)",
                {"project_id": project_id,
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
