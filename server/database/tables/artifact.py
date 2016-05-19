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
import datetime
from typing import List, Optional


class ArtifactTable(Table):
    """
    Base class for "artifact" table

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
        Table.__init__(self)

    def create(self, connection: Connection) -> None:
        """
        Creates the table

        :param connection:  Database connection
        """
        raise NotImplementedError()

    def read_all_ids(self, connection: Connection, tracker_id: int) -> List[int]:
        """
        Reads IDs of all artifacts in the database that belong to the specified tracker

        :param connection:  Database connection
        :param tracker_id:  ID of the tracker

        :return:    List of tracker IDs
        """
        raise NotImplementedError()

    def read_artifact(self, connection: Connection, artifact_id: int) -> Optional[dict]:
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
        raise NotImplementedError()

    def insert_row(self, connection: Connection,
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
        raise NotImplementedError()
