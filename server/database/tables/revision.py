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


class RevisionTable(Table):
    """
    Base class for "revision" table

    Table's columns:

    - id:           int
    - timestamp:    datetime
    - user_id:      int, references user.id
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

    def read_current_revision_id(self, connection: Connection) -> Optional[int]:
        """
        Reads the current revision ID from the database

        :param connection:  Database connection

        :return:    ID of the current revision
        """
        raise NotImplementedError()

    def read_revision(self, connection: Connection, revision_id: int) -> Optional[dict]:
        """
        Reads the revision information from the database

        :param connection:  Database connection
        :param revision_id: ID of the revision to read

        :return:    Revision information

        Returned dictionary contains items:

        - id
        - timestamp
        - user_id
        """
        raise NotImplementedError()

    def read_revisions_by_id_range(self,
                                   connection: Connection,
                                   min_revision_id: int,
                                   max_revision_id: int) -> List[dict]:
        """
        Reads the revision information from the database

        :param connection:      Database connection
        :param min_revision_id: Smallest revision ID to be included
        :param max_revision_id: Biggest revision ID to be included

        :return:    List of revisions

        Each dictionary in the returned list contains items:

        - id
        - timestamp
        - user_id
        """
        raise NotImplementedError()

    def read_revisions_by_time_range(self,
                                     connection: Connection,
                                     min_timestamp: datetime.datetime,
                                     max_timestamp: datetime.datetime) -> List[dict]:
        """
        Reads the revision information from the database

        :param connection:      Database connection
        :param min_timestamp:   Earliest timestamp to be included
        :param max_timestamp:   Latest timestamp to be included

        :return:    List of revisions

        Each dictionary in the returned list contains items:

        - id
        - timestamp
        - user_id
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   timestamp: datetime.datetime,
                   user_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:  Database connection
        :param timestamp:   Timestamp
        :param user_id:     ID of the user

        :return:    ID of the newly created row
        """
        raise NotImplementedError()
