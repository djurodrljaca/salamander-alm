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


class ArtifactSelection(enum.Enum):
    """
    Artifact selection
    """
    Active = 1,
    Inactive = 2,
    All = 3


class ArtifactInformationTable(Table):
    """
    Base class for "artifact_information" table

    Table's columns:

    - id:           int
    - artifact_id:  int, references artifact.id
    - locked:       bool
    - active:       bool
    - revision_id:  int, references revision.id
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

    def read_all_artifact_ids(self,
                              connection: Connection,
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
        raise NotImplementedError()

    def read_information(self,
                         connection: Connection,
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
        - locked
        - active
        - revision_id
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
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
        raise NotImplementedError()
