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


class TrackerFieldSelection(enum.Enum):
    """
    Tracker field selection
    """
    Active = 1,
    Inactive = 2,
    All = 3


class TrackerFieldInformationTable(Table):
    """
    Base class for "tracker_field_information" table

    Table's columns:

    - id:               int
    - tracker_field_id: int, references tracker_field.id
    - name:             str
    - display_name:     str
    - description:      Optional[str]
    - active:           bool
    - revision_id:      int, references revision.id
    """

# TODO: add "type" column!

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

    def read_all_tracker_field_ids(self,
                                   connection: Connection,
                                   tracker_id: int,
                                   tracker_field_selection: TrackerFieldSelection,
                                   max_revision_id: int) -> List[int]:
        """
        Reads IDs of all tracker field IDs in the database that belong to the specified tracker

        :param connection:              Database connection
        :param tracker_id:              ID of the tracker
        :param tracker_field_selection: Search for active, inactive or all trackers
        :param max_revision_id:         Maximum revision ID for the search

        :return:    List of tracker field IDs
        """
        raise NotImplementedError()

    def read_information(self,
                         connection: Connection,
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
        - active
        - revision_id
        """
        raise NotImplementedError()

    def insert_row(self,
                   connection: Connection,
                   tracker_field_id: int,
                   name: str,
                   display_name: str,
                   description: str,
                   active: bool,
                   revision_id: int) -> Optional[int]:
        """
        Inserts a new row in the table

        :param connection:          Database connection
        :param tracker_field_id:    ID of the tracker field
        :param name:                Tracker field name
        :param display_name:        Tracker field display name
        :param description:         Tracker field description
        :param active:              State of the tracker field (active or inactive)
        :param revision_id:         Revision ID

        :return:    ID of the newly created row
        """
        raise NotImplementedError()
