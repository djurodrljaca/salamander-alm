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
from database.tables.project import ProjectTable
from typing import List, Optional


class ProjectTableSqlite(ProjectTable):
    """
    Implementation of "project" table for SQLite database
    """

    def __init__(self):
        """
        Constructor
        """
        ProjectTable.__init__(self)

    def create(self, connection: ConnectionSqlite) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        connection.native_connection.execute(
            "CREATE TABLE project (\n"
            "    id INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "               NOT NULL\n"
            ")")

    def read_all_projects(self, connection: ConnectionSqlite) -> List[int]:
        """
        Reads IDs of all projects in the database

        :param connection:  Database connection

        :return:    List of project IDs
        """
        cursor = connection.native_connection.execute(
            "SELECT id\n"
            "FROM project")

        projects = list()

        for row in cursor.fetchall():
            projects.append(row[0])

        return projects

    def insert_row(self, connection: ConnectionSqlite) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection

        :return:    ID of the newly created row
        """
        cursor = connection.native_connection.execute(
            "INSERT INTO project\n"
            "   (id)\n"
            "VALUES (NULL)")

        return cursor.lastrowid
