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
from database.database import DatabaseInterface
from database.tables.tracker_field_information import TrackerFieldSelection
import datetime
from typing import List, Optional


class TrackerFieldManagementInterface(object):
    """
    Tracker field management

    Dependencies:

    - DatabaseInterface
    """
    
    def __init__(self):
        """
        Constructor is disabled!
        """
        raise RuntimeError()
    
    @staticmethod
    def read_all_tracker_field_ids(tracker_id: int,
                                   tracker_field_selection=TrackerFieldSelection.Active,
                                   max_revision_id=None) -> List[int]:
        """
        Reads all tracker field IDs from the database

        :param tracker_id:              ID of the tracker
        :param tracker_field_selection: Search for active, inactive or all tracker
        :param max_revision_id:         Maximum revision ID for the search ("None" for latest
                                        revision)

        :return:    List of tracker field IDs
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Reads all tracker field IDs from the database
        tracker_fields = None
        
        if max_revision_id is not None:
            tracker_fields = \
                DatabaseInterface.tables().tracker_field_information.read_all_tracker_field_ids(
                    connection,
                    tracker_id,
                    tracker_field_selection,
                    max_revision_id)
        
        return tracker_fields
    
    @staticmethod
    def read_tracker_field_by_id(tracker_field_id: int,
                                 max_revision_id=None) -> Optional[dict]:
        """
        Reads a tracker field (active or inactive) that matches the specified tracker field ID

        :param tracker_field_id:    ID of the tracker
        :param max_revision_id:     Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker field that matches the specified tracker field ID
        tracker_field = None
        
        if max_revision_id is not None:
            tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_id(
                connection,
                tracker_field_id,
                max_revision_id)
        
        return tracker_field

    @staticmethod
    def read_tracker_field_by_name(name: str, max_revision_id=None) -> Optional[dict]:
        """
        Reads an active tracker field that matches the specified name

        :param name:            Tracker field's name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker field that matches the specified name
        tracker_field = None
        
        if max_revision_id is not None:
            tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_name(
                connection,
                name,
                max_revision_id)
        
        return tracker_field
    
    @staticmethod
    def read_tracker_fields_by_name(name: str, max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive tracker fields that match the specified name

        :param name:            Tracker field's short name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker field information of all tracker fields that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read tracker fields that match the specified name
        tracker_fields = list()
        
        if max_revision_id is not None:
            tracker_field_information_list = \
                DatabaseInterface.tables().tracker_field_information.read_information(
                    connection,
                    "name",
                    name,
                    TrackerFieldSelection.All,
                    max_revision_id)

            for tracker_field_information in tracker_field_information_list:
                tracker_fields.append(
                    TrackerFieldManagementInterface.__parse_tracker_field_information(
                        tracker_field_information))

        return tracker_fields
    
    @staticmethod
    def read_tracker_field_by_display_name(display_name: str,
                                           max_revision_id=None) -> Optional[dict]:
        """
        Reads an active tracker field that matches the specified display name

        :param display_name:    Tracker field's display name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker field that matches the specified display name
        tracker_field = None
        
        if max_revision_id is not None:
            tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_display_name(
                connection,
                display_name,
                max_revision_id)
        
        return tracker_field
    
    @staticmethod
    def read_tracker_fields_by_display_name(display_name: str,
                                            max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive tracker fields that match the specified display name

        :param display_name:    Tracker field's full name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker field information of all tracker fields that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read tracker fields that match the specified display name
        tracker_fields = list()
        
        if max_revision_id is not None:
            tracker_field_information_list = \
                DatabaseInterface.tables().tracker_field_information.read_information(
                    connection,
                    "display_name",
                    display_name,
                    TrackerFieldSelection.All,
                    max_revision_id)
            
            for tracker_field_information in tracker_field_information_list:
                tracker_fields.append(
                    TrackerFieldManagementInterface.__parse_tracker_field_information(
                        tracker_field_information))
        
        return tracker_fields

    # TODO: implement create_tracker_fields() !

    @staticmethod
    def create_tracker_field(requested_by_user: int,
                             tracker_id: int,
                             name: str,
                             display_name: str,
                             description: str) -> Optional[int]:
        """
        Creates a new tracker

        :param requested_by_user:   ID of the user that requested creation of the new tracker field
        :param tracker_id:          ID of the tracker
        :param name:                Tracker's name
        :param display_name:        Tracker's display name
        :param description:         Tracker's description

        :return:    Tracker field ID of the new tracker field
        """
        tracker_field_id = None
        connection = DatabaseInterface.create_connection()
        
        try:
            success = connection.begin_transaction()
            
            # Start a new revision
            revision_id = None
            
            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)
                
                if revision_id is None:
                    success = False
            
            # Create the tracker
            if success:
                tracker_field_id = TrackerFieldManagementInterface.__create_tracker_field(
                    connection,
                    tracker_id,
                    name,
                    display_name,
                    description,
                    revision_id)
                
                if tracker_field_id is None:
                    success = False
            
            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise
        
        return tracker_field_id
    
    @staticmethod
    def update_tracker_field_information(requested_by_user: int,
                                         tracker_field_to_modify: int,
                                         name: str,
                                         display_name: str,
                                         description: str,
                                         active: bool) -> bool:
        """
        Updates tracker's information

        :param requested_by_user:       ID of the user that requested modification of the user
        :param tracker_field_to_modify: ID of the tracker field that should be modified
        :param name:                    Tracker field's new name
        :param display_name:            Tracker field's new display name
        :param description:             Tracker field's new description
        :param active:                  Tracker field's new state (active or inactive)

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()
        
        try:
            success = connection.begin_transaction()
            
            # Start a new revision
            revision_id = None
            
            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)
                
                if revision_id is None:
                    success = False
            
            # Check if there is already an existing tracker field with the same name
            if success:
                tracker = TrackerFieldManagementInterface.__read_tracker_field_by_name(connection,
                                                                                       name,
                                                                                       revision_id)
                
                if tracker is not None:
                    if tracker["id"] != tracker_field_to_modify:
                        success = False
            
            # Check if there is already an existing tracker field with the same display name
            if success:
                tracker = TrackerFieldManagementInterface.__read_tracker_field_by_display_name(
                    connection,
                    display_name,
                    revision_id)
                
                if tracker is not None:
                    if tracker["id"] != tracker_field_to_modify:
                        success = False
            
            # Update tracker field's information in the new revision
            if success:
                row_id = DatabaseInterface.tables().tracker_field_information.insert_row(
                    connection,
                    tracker_field_to_modify,
                    name,
                    display_name,
                    description,
                    active,
                    revision_id)
                
                if row_id is None:
                    success = False
            
            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise
        
        return success
    
    @staticmethod
    def activate_tracker_field(requested_by_user: int, tracker_field_id: int) -> bool:
        """
        Activates an inactive tracker field

        :param requested_by_user:   ID of the user that requested modification of the user
        :param tracker_field_id:    ID of the tracker field that should be activated

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()
        
        try:
            success = connection.begin_transaction()
            
            # Start a new revision
            revision_id = None
            
            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)
                
                if revision_id is None:
                    success = False
            
            # Read tracker field
            tracker_field = None
            
            if success:
                tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_id(
                    connection,
                    tracker_field_id,
                    revision_id)
                
                if tracker_field is None:
                    success = False
                elif tracker_field["active"]:
                    # Error, tracker field is already active
                    success = False
            
            # Activate tracker field
            if success:
                success = DatabaseInterface.tables().tracker_field_information.insert_row(
                    connection,
                    tracker_field_id,
                    tracker_field["name"],
                    tracker_field["display_name"],
                    tracker_field["description"],
                    True,
                    revision_id)
            
            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise
        
        return success
    
    @staticmethod
    def deactivate_tracker_field(requested_by_user: int, tracker_field_id: int) -> bool:
        """
        Deactivates an active tracker field

        :param requested_by_user:   ID of the user that requested modification of the user
        :param tracker_field_id:    ID of the tracker field that should be deactivated

        :return:    Success or failure
        """
        connection = DatabaseInterface.create_connection()
        
        try:
            success = connection.begin_transaction()
            
            # Start a new revision
            revision_id = None
            
            if success:
                revision_id = DatabaseInterface.tables().revision.insert_row(
                    connection,
                    datetime.datetime.utcnow(),
                    requested_by_user)
                
                if revision_id is None:
                    success = False
            
            # Read tracker field
            tracker_field = None
            
            if success:
                tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_id(
                    connection,
                    tracker_field_id,
                    revision_id)
                
                if tracker_field is None:
                    success = False
                elif not tracker_field["active"]:
                    # Error, tracker field is already inactive
                    success = False
            
            # Deactivate tracker field
            if success:
                success = DatabaseInterface.tables().tracker_field_information.insert_row(
                    connection,
                    tracker_field_id,
                    tracker_field["name"],
                    tracker_field["display_name"],
                    tracker_field["description"],
                    False,
                    revision_id)
            
            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise
        
        return success
    
    @staticmethod
    def __read_tracker_field_by_id(connection: Connection,
                                   tracker_field_id: int,
                                   max_revision_id: int) -> Optional[dict]:
        """
        Reads a tracker field (active or inactive) that matches the search parameters

        :param connection:          Database connection
        :param tracker_field_id:    ID of the tracker
        :param max_revision_id:     Maximum revision ID for the search

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        # Read the tracker fields that match the search attribute
        tracker_fields = DatabaseInterface.tables().tracker_field_information.read_information(
            connection,
            "tracker_field_id",
            tracker_field_id,
            TrackerFieldSelection.All,
            max_revision_id)
        
        # Return a tracker field only if exactly one was found
        tracker_field = None
        
        if tracker_fields is not None:
            if len(tracker_fields) == 1:
                tracker_field = {"id": tracker_fields[0]["tracker_field_id"],
                                 "tracker_id": tracker_fields[0]["tracker_id"],
                                 "name": tracker_fields[0]["name"],
                                 "display_name": tracker_fields[0]["display_name"],
                                 "description": tracker_fields[0]["description"],
                                 "active": tracker_fields[0]["active"],
                                 "revision_id": tracker_fields[0]["revision_id"]}
        
        return tracker_field

    @staticmethod
    def __read_tracker_field_by_name(connection: Connection,
                                     name: str,
                                     max_revision_id: int) -> Optional[dict]:
        """
        Reads an active tracker field that matches the specified name

        :param connection:      Database connection
        :param name:            Tracker field's name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        # Read the tracker fields that match the search attribute
        tracker_fields = DatabaseInterface.tables().tracker_field_information.read_information(
            connection,
            "name",
            name,
            TrackerFieldSelection.Active,
            max_revision_id)

        # Return a tracker field only if exactly one was found
        tracker_field = None

        if tracker_fields is not None:
            if len(tracker_fields) == 1:
                tracker_field = {"id": tracker_fields[0]["tracker_field_id"],
                                 "tracker_id": tracker_fields[0]["tracker_id"],
                                 "name": tracker_fields[0]["name"],
                                 "display_name": tracker_fields[0]["display_name"],
                                 "description": tracker_fields[0]["description"],
                                 "active": tracker_fields[0]["active"],
                                 "revision_id": tracker_fields[0]["revision_id"]}

        return tracker_field
    
    @staticmethod
    def __read_tracker_field_by_display_name(connection: Connection,
                                             display_name: str,
                                             max_revision_id: int) -> Optional[dict]:
        """
        Reads an active tracker that matches the specified full name

        :param connection:      Database connection
        :param display_name:    Tracker's display name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Tracker field information object

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        # Read the tracker fields that match the search attribute
        tracker_fields = DatabaseInterface.tables().tracker_field_information.read_information(
            connection,
            "display_name",
            display_name,
            TrackerFieldSelection.Active,
            max_revision_id)

        # Return a tracker field only if exactly one was found
        tracker_field = None

        if tracker_fields is not None:
            if len(tracker_fields) == 1:
                tracker_field = {"id": tracker_fields[0]["tracker_field_id"],
                                 "tracker_id": tracker_fields[0]["tracker_id"],
                                 "name": tracker_fields[0]["name"],
                                 "display_name": tracker_fields[0]["display_name"],
                                 "description": tracker_fields[0]["description"],
                                 "active": tracker_fields[0]["active"],
                                 "revision_id": tracker_fields[0]["revision_id"]}

        return tracker_field
    
    @staticmethod
    def __create_tracker_field(connection: Connection,
                               tracker_id: int,
                               name: str,
                               display_name: str,
                               description: str,
                               revision_id: int) -> Optional[int]:
        """
        Creates a new tracker field

        :param connection:      Database connection
        :param tracker_id:      ID of the tracker
        :param name:            Tracker field's name
        :param display_name:    Tracker field's display name
        :param description:     Tracker field's description
        :param revision_id:     Revision ID

        :return:    Tracker field ID of the newly created tracker field
        """
        # Check if a tracker field with the same name already exists
        tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_name(connection,
                                                                                     name,
                                                                                     revision_id)
        
        if tracker_field is not None:
            return None
        
        # Check if a tracker field with the same display name already exists
        tracker_field = TrackerFieldManagementInterface.__read_tracker_field_by_display_name(
            connection,
            display_name,
            revision_id)
        
        if tracker_field is not None:
            return None
        
        # Create the tracker field in the new revision
        tracker_field_id = DatabaseInterface.tables().tracker_field.insert_row(connection,
                                                                               tracker_id)
        
        if tracker_field_id is None:
            return None
        
        # Add tracker field information to the tracker field
        tracker_field_information_id = \
            DatabaseInterface.tables().tracker_field_information.insert_row(
                connection,
                tracker_field_id,
                name,
                display_name,
                description,
                True,
                revision_id)
        
        if tracker_field_information_id is None:
            return None
        
        return tracker_field_id
    
    @staticmethod
    def __parse_tracker_field_information(raw_tracker_field_information: dict) -> dict:
        """
        Parse raw tracker field information object and convert it to a tracker field information
        object

        :param raw_tracker_field_information:   Tracker field information

        :return:    Tracker field information object

        Input (raw) dictionary contains items:

        - tracker_id
        - tracker_field_id
        - name
        - display_name
        - description
        - active
        - revision_id

        Returned dictionary contains items:

        - id
        - tracker_id
        - name
        - display_name
        - description
        - active
        - revision_id
        """
        return {"id": raw_tracker_field_information["tracker_field_id"],
                "tracker_id": raw_tracker_field_information["tracker_id"],
                "name": raw_tracker_field_information["name"],
                "display_name": raw_tracker_field_information["display_name"],
                "description": raw_tracker_field_information["description"],
                "active": raw_tracker_field_information["active"],
                "revision_id": raw_tracker_field_information["revision_id"]}
