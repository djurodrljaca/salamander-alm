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

from database.connection import Connection
from database.table import Table
import enum
from typing import Any, List, Optional


class ProjectSelection(enum.Enum):
    """
    Project selection
    """
    Active = 1,
    Inactive = 2,
    All = 3


class ProjectInformationTable(Table):
    """
    Base class for "project_information" table

    Table's columns:

    - id:           int
    - project_id:   int
    - short_name:   str
    - full_name:    str
    - description:  Optional[str]
    - active:       bool
    - revision_id:  int
    """

    def __init__(self):
        """
        Constructor
        """
        Table.__init__(self)

    def create(self, connection: Connection) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        raise NotImplementedError()

    def read_all_project_ids(self,
                             connection: Connection,
                             project_selection: ProjectSelection,
                             max_revision_id: int) -> List[int]:
        """
        Reads IDs of all project IDs in the database

        :param connection:          Database connection
        :param project_selection:   Search for active, inactive or all projects
        :param max_revision_id:     Maximum revision ID for the search

        :return:    List of project IDs
        """
        raise NotImplementedError()

    def read_information(self,
                         connection: Connection,
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
        - short name
        - full name

        Each dictionary in the returned list contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
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
        :param short_name:  Project name
        :param full_name:   Project name
        :param description: Project description
        :param active:      State of the project (active or inactive)
        :param revision_id: Revision ID

        :return:    ID of the newly created row
        """
        raise NotImplementedError()
