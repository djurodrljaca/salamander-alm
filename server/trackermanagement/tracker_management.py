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
from database.tables.tracker_information import TrackerSelection
import datetime
from typing import List, Optional


class TrackerManagementInterface(object):
    """
    Tracker management

    Dependencies:

    - DatabaseInterface
    """
    
    def __init__(self):
        """
        Constructor is disabled!
        """
        raise RuntimeError()
    
    @staticmethod
    def read_all_tracker_ids(project_id: int,
                             tracker_selection=TrackerSelection.Active,
                             max_revision_id=None) -> List[int]:
        """
        Reads all tracker IDs from the database

        :param project_id:          ID of the project
        :param tracker_selection:   Search for active, inactive or all tracker
        :param max_revision_id:     Maximum revision ID for the search ("None" for latest revision)

        :return:    List of tracker IDs
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Reads all tracker IDs from the database
        trackers = None
        
        if max_revision_id is not None:
            trackers = DatabaseInterface.tables().tracker_information.read_all_tracker_ids(
                connection,
                project_id,
                tracker_selection,
                max_revision_id)
        
        return trackers
    
    @staticmethod
    def read_tracker_by_id(tracker_id: int, max_revision_id=None) -> Optional[dict]:
        """
        Reads a tracker (active or inactive) that matches the specified tracker ID

        :param tracker_id:      ID of the tracker
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker that matches the specified tracker ID
        tracker = None
        
        if max_revision_id is not None:
            tracker = TrackerManagementInterface.__read_tracker_by_id(connection,
                                                                      tracker_id,
                                                                      max_revision_id)
        
        return tracker
    
    @staticmethod
    def read_tracker_by_short_name(short_name: str, max_revision_id=None) -> Optional[dict]:
        """
        Reads an active tracker that matches the specified short name

        :param short_name:      Tracker's short name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker that matches the specified short name
        tracker = None
        
        if max_revision_id is not None:
            tracker = TrackerManagementInterface.__read_tracker_by_short_name(connection,
                                                                              short_name,
                                                                              max_revision_id)
        
        return tracker
    
    @staticmethod
    def read_trackers_by_short_name(short_name: str,
                                    max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive trackers that match the specified short name

        :param short_name:      Tracker's short name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker information of all trackers that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read trackers that match the specified short name
        trackers = list()
        
        if max_revision_id is not None:
            tracker_information_list = \
                DatabaseInterface.tables().tracker_information.read_information(
                    connection,
                    "short_name",
                    short_name,
                    TrackerSelection.All,
                    max_revision_id)

            for tracker_information in tracker_information_list:
                trackers.append(TrackerManagementInterface.__parse_tracker_information(
                    tracker_information))

        return trackers
    
    @staticmethod
    def read_tracker_by_full_name(full_name: str,
                                  max_revision_id=None) -> Optional[dict]:
        """
        Reads an active tracker that matches the specified full name

        :param full_name:       Tracker's full name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read a tracker that matches the specified full name
        tracker = None
        
        if max_revision_id is not None:
            tracker = TrackerManagementInterface.__read_tracker_by_full_name(connection,
                                                                             full_name,
                                                                             max_revision_id)
        
        return tracker
    
    @staticmethod
    def read_trackers_by_full_name(full_name: str,
                                   max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive trackers that match the specified full name

        :param full_name:       Tracker's full name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Tracker information of all trackers that match the search attribute

        Each dictionary in the returned list contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        connection = DatabaseInterface.create_connection()
        
        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)
        
        # Read trackers that match the specified full name
        trackers = list()
        
        if max_revision_id is not None:
            tracker_information_list = \
                DatabaseInterface.tables().tracker_information.read_information(
                    connection,
                    "full_name",
                    full_name,
                    TrackerSelection.All,
                    max_revision_id)
            
            for tracker_information in tracker_information_list:
                trackers.append(TrackerManagementInterface.__parse_tracker_information(
                    tracker_information))
        
        return trackers
    
    @staticmethod
    def create_tracker(requested_by_user: int,
                       project_id: int,
                       short_name: str,
                       full_name: str,
                       description: str) -> Optional[int]:
        """
        Creates a new tracker

        :param requested_by_user:   ID of the user that requested creation of the new tracker
        :param project_id:          ID of the project
        :param short_name:          Tracker's short name
        :param full_name:           Tracker's full name
        :param description:         Tracker's description

        :return:    Tracker ID of the new tracker
        """
        tracker_id = None
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
                tracker_id = TrackerManagementInterface.__create_tracker(connection,
                                                                         project_id,
                                                                         short_name,
                                                                         full_name,
                                                                         description,
                                                                         revision_id)
                
                if tracker_id is None:
                    success = False
            
            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise
        
        return tracker_id
    
    @staticmethod
    def update_tracker_information(requested_by_user: int,
                                   tracker_to_modify: int,
                                   short_name: str,
                                   full_name: str,
                                   description: str,
                                   active: bool) -> bool:
        """
        Updates tracker's information

        :param requested_by_user:   ID of the user that requested modification of the user
        :param tracker_to_modify:   ID of the tracker that should be modified
        :param short_name:          Tracker's new short name
        :param full_name:           Tracker's new full name
        :param description:         Tracker's new description
        :param active:              Tracker's new state (active or inactive)

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
            
            # Check if there is already an existing tracker with the same short name
            if success:
                tracker = TrackerManagementInterface.__read_tracker_by_short_name(connection,
                                                                                  short_name,
                                                                                  revision_id)
                
                if tracker is not None:
                    if tracker["id"] != tracker_to_modify:
                        success = False
            
            # Check if there is already an existing tracker with the same full name
            if success:
                tracker = TrackerManagementInterface.__read_tracker_by_full_name(connection,
                                                                                 full_name,
                                                                                 revision_id)
                
                if tracker is not None:
                    if tracker["id"] != tracker_to_modify:
                        success = False
            
            # Update tracker's information in the new revision
            if success:
                row_id = DatabaseInterface.tables().tracker_information.insert_row(
                    connection,
                    tracker_to_modify,
                    short_name,
                    full_name,
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
    def activate_tracker(requested_by_user: int, tracker_id: int) -> bool:
        """
        Activates an inactive tracker

        :param requested_by_user:   ID of the user that requested modification of the user
        :param tracker_id:          ID of the tracker that should be activated

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
            
            # Read tracker
            tracker = None
            
            if success:
                tracker = TrackerManagementInterface.__read_tracker_by_id(connection,
                                                                          tracker_id,
                                                                          revision_id)
                
                if tracker is None:
                    success = False
                elif tracker["active"]:
                    # Error, tracker is already active
                    success = False
            
            # Activate tracker
            if success:
                success = DatabaseInterface.tables().tracker_information.insert_row(
                    connection,
                    tracker_id,
                    tracker["short_name"],
                    tracker["full_name"],
                    tracker["description"],
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
    def deactivate_tracker(requested_by_user: int, tracker_id: int) -> bool:
        """
        Deactivates an active tracker

        :param requested_by_user:   ID of the user that requested modification of the user
        :param tracker_id:          ID of the tracker that should be deactivated

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
            
            # Read tracker
            tracker = None
            
            if success:
                tracker = TrackerManagementInterface.__read_tracker_by_id(connection,
                                                                          tracker_id,
                                                                          revision_id)
                
                if tracker is None:
                    success = False
                elif not tracker["active"]:
                    # Error, tracker is already inactive
                    success = False
            
            # Deactivate tracker
            if success:
                success = DatabaseInterface.tables().tracker_information.insert_row(
                    connection,
                    tracker_id,
                    tracker["short_name"],
                    tracker["full_name"],
                    tracker["description"],
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
    def __read_tracker_by_id(connection: Connection,
                             tracker_id: int,
                             max_revision_id: int) -> Optional[dict]:
        """
        Reads a tracker (active or inactive) that matches the search parameters

        :param connection:      Database connection
        :param tracker_id:      ID of the tracker
        :param max_revision_id: Maximum revision ID for the search

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the trackers that match the search attribute
        trackers = DatabaseInterface.tables().tracker_information.read_information(
            connection,
            "tracker_id",
            tracker_id,
            TrackerSelection.All,
            max_revision_id)
        
        # Return a tracker only if exactly one was found
        tracker = None
        
        if trackers is not None:
            if len(trackers) == 1:
                tracker = {"id": trackers[0]["tracker_id"],
                           "project_id": trackers[0]["project_id"],
                           "short_name": trackers[0]["short_name"],
                           "full_name": trackers[0]["full_name"],
                           "description": trackers[0]["description"],
                           "active": trackers[0]["active"],
                           "revision_id": trackers[0]["revision_id"]}
        
        return tracker
    
    @staticmethod
    def __read_tracker_by_short_name(connection: Connection,
                                     short_name: str,
                                     max_revision_id: int) -> Optional[dict]:
        """
        Reads an active tracker that matches the specified short name

        :param connection:      Database connection
        :param short_name:      Tracker's short name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the trackers that match the search attribute
        trackers = DatabaseInterface.tables().tracker_information.read_information(
            connection,
            "short_name",
            short_name,
            TrackerSelection.Active,
            max_revision_id)
        
        # Return a tracker only if exactly one was found
        tracker = None
        
        if trackers is not None:
            if len(trackers) == 1:
                tracker = {"id": trackers[0]["tracker_id"],
                           "project_id": trackers[0]["project_id"],
                           "short_name": trackers[0]["short_name"],
                           "full_name": trackers[0]["full_name"],
                           "description": trackers[0]["description"],
                           "active": trackers[0]["active"],
                           "revision_id": trackers[0]["revision_id"]}
        
        return tracker
    
    @staticmethod
    def __read_tracker_by_full_name(connection: Connection,
                                    full_name: str,
                                    max_revision_id: int) -> Optional[dict]:
        """
        Reads an active tracker that matches the specified full name

        :param connection:      Database connection
        :param full_name:       Tracker's full name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Tracker information object

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the trackers that match the search attribute
        trackers = DatabaseInterface.tables().tracker_information.read_information(
            connection,
            "full_name",
            full_name,
            TrackerSelection.Active,
            max_revision_id)
        
        # Return a tracker only if exactly one was found
        tracker = None
        
        if trackers is not None:
            if len(trackers) == 1:
                tracker = {"id": trackers[0]["tracker_id"],
                           "project_id": trackers[0]["project_id"],
                           "short_name": trackers[0]["short_name"],
                           "full_name": trackers[0]["full_name"],
                           "description": trackers[0]["description"],
                           "active": trackers[0]["active"],
                           "revision_id": trackers[0]["revision_id"]}
        
        return tracker
    
    @staticmethod
    def __create_tracker(connection: Connection,
                         project_id: int,
                         short_name: str,
                         full_name: str,
                         description: str,
                         revision_id: int) -> Optional[int]:
        """
        Creates a new tracker

        :param connection:  Database connection
        :param project_id:  ID of the project
        :param short_name:  Tracker's short name
        :param full_name:   Tracker's full name
        :param description: Tracker's description
        :param revision_id: Revision ID

        :return:    Tracker ID of the newly created tracker
        """
        # Check if a tracker with the same short name already exists
        tracker = TrackerManagementInterface.__read_tracker_by_short_name(connection,
                                                                          short_name,
                                                                          revision_id)
        
        if tracker is not None:
            return None
        
        # Check if a tracker with the same full name already exists
        tracker = TrackerManagementInterface.__read_tracker_by_full_name(connection,
                                                                         full_name,
                                                                         revision_id)
        
        if tracker is not None:
            return None
        
        # Create the tracker in the new revision
        tracker_id = DatabaseInterface.tables().tracker.insert_row(connection, project_id)
        
        if tracker_id is None:
            return None
        
        # Add tracker information to the tracker
        tracker_information_id = DatabaseInterface.tables().tracker_information.insert_row(
            connection,
            tracker_id,
            short_name,
            full_name,
            description,
            True,
            revision_id)
        
        if tracker_information_id is None:
            return None
        
        return tracker_id
    
    @staticmethod
    def __parse_tracker_information(raw_tracker_information: dict) -> dict:
        """
        Parse raw tracker information object and convert it to a tracker information object

        :param raw_tracker_information: Tracker information

        :return:    Tracker information object

        Input (raw) dictionary contains items:

        - project_id
        - tracker_id
        - short_name
        - full_name
        - description
        - active
        - revision_id

        Returned dictionary contains items:

        - id
        - project_id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        return {"id": raw_tracker_information["tracker_id"],
                "project_id": raw_tracker_information["project_id"],
                "short_name": raw_tracker_information["short_name"],
                "full_name": raw_tracker_information["full_name"],
                "description": raw_tracker_information["description"],
                "active": raw_tracker_information["active"],
                "revision_id": raw_tracker_information["revision_id"]}
