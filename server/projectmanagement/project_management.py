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
import datetime
from typing import List, Optional
from usermanagement.user_management import UserManagementInterface


class ProjectManagementInterface(object):
    """
    User management

    Dependencies:
    - DatabaseInterface
    - UserManagementInterface
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def __del__(self):
        """
        Destructor
        """
        pass

    @staticmethod
    def read_all_project_ids() -> List[int]:
        """
        Reads all project IDs from the database

        :return:    List of project IDs

        NOTE:   This method searches both active and inactive project
        """
        connection = DatabaseInterface.create_connection()
        return DatabaseInterface.tables().project.read_all_projects(connection)

    @staticmethod
    def read_project_by_id(project_id: int) -> Optional[dict]:
        """
        Reads a project that matches the specified project ID

        :param project_id:  ID of the user

        :return:    Project information object

        NOTE:   This method searches both active and inactive projects
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read a project that matches the specified project ID
        user = None

        if current_revision_id is not None:
            user = ProjectManagementInterface.__read_project_by_id(connection,
                                                                   project_id,
                                                                   current_revision_id)

        return user

    @staticmethod
    def read_project_by_short_name(short_name: str) -> Optional[dict]:
        """
        Reads a project that matches the specified short name

        :param short_name:  Project's short name

        :return:    Project information object

        NOTE:   This method only searches active projects
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read a project that matches the specified short name
        project = None

        if current_revision_id is not None:
            project = ProjectManagementInterface.__read_project_by_short_name(connection,
                                                                              short_name,
                                                                              current_revision_id)

        return project

    @staticmethod
    def read_projects_by_short_name(short_name: str, only_active_projects: bool) -> List[dict]:
        """
        Reads a project that matches the specified short name

        :param short_name:              Project's short name
        :param only_active_projects:    Only search for active projects

        :return:    Project information object
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read projects that match the specified short name
        projects = list()

        if current_revision_id is not None:
            projects = DatabaseInterface.tables().project_information.read_information(
                connection,
                "short_name",
                short_name,
                only_active_projects,
                current_revision_id)

        return projects

    @staticmethod
    def read_project_by_full_name(full_name: str) -> Optional[dict]:
        """
        Reads a project that matches the specified full name

        :param full_name:  Project's full name

        :return:    Project information object

        NOTE:   This method only searches active projects
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read a project that matches the specified full name
        project = None

        if current_revision_id is not None:
            project = ProjectManagementInterface.__read_project_by_full_name(connection,
                                                                             full_name,
                                                                             current_revision_id)

        return project

    @staticmethod
    def read_projects_by_full_name(full_name: str, only_active_projects=True) -> List[dict]:
        """
        Reads a user that matches the specified user ID

        :param full_name:               Projects's full name
        :param only_active_projects:    Only search for active projects

        :return:    Project information object
        """
        # First get the current revision
        connection = DatabaseInterface.create_connection()
        current_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
            connection)

        # Read projects that match the specified full name
        projects = list()

        if current_revision_id is not None:
            projects = DatabaseInterface.tables().project_information.read_information(
                connection,
                "full_name",
                full_name,
                only_active_projects,
                current_revision_id)

        return projects

    @staticmethod
    def create_project(requested_by_user: int,
                       short_name: str,
                       full_name: str,
                       description: str) -> Optional[int]:
        """
        Create a new user

        :param requested_by_user:   ID of the user that requested creation of the new project
        :param short_name:          Project's short name
        :param full_name:           Project's full name
        :param description:         Project's description

        :return:    Project ID of the new project
        """
        project_id = None
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

            # Create the project
            if success:
                project_id = ProjectManagementInterface.__create_project(connection,
                                                                         short_name,
                                                                         full_name,
                                                                         description,
                                                                         revision_id)

                if project_id is None:
                    success = False

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            raise

        return project_id

    @staticmethod
    def update_project_information(requested_by_user: int,
                                   project_to_modify: int,
                                   short_name: str,
                                   full_name: str,
                                   description: str,
                                   active: bool) -> bool:
        """
        Update project's information

        :param requested_by_user:   ID of the user that requested modification of the user
        :param project_to_modify:   ID of the user that should be modified
        :param short_name:          Project's new short name
        :param full_name:           Project's new full name
        :param description:         Project's new description
        :param active:              Project's new state (active or inactive)

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

            # Check if there is already an existing project with the same short name
            if success:
                project = ProjectManagementInterface.__read_project_by_short_name(connection,
                                                                                  short_name,
                                                                                  revision_id)

                if project is not None:
                    if project["project_id"] != project_to_modify:
                        success = False

            # Check if there is already an existing project with the same full name
            if success:
                project = ProjectManagementInterface.__read_project_by_full_name(connection,
                                                                                 full_name,
                                                                                 revision_id)

                if project is not None:
                    if project["project_id"] != project_to_modify:
                        success = False

            # Update project's information in the new revision
            if success:
                row_id = DatabaseInterface.tables().project_information.insert_row(
                    connection,
                    project_to_modify,
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
    def __read_project_by_id(connection: Connection,
                             project_id: int,
                             max_revision_id: int) -> Optional[dict]:
        """
        Reads a project that matches the search parameters

        :param connection:      Database connection
        :param project_id:      ID of the project
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(connection,
                                                                                   "project_id",
                                                                                   project_id,
                                                                                   False,
                                                                                   max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = projects[0]

        return project

    @staticmethod
    def __read_project_by_short_name(connection: Connection,
                                     short_name: str,
                                     max_revision_id: int) -> Optional[dict]:
        """
        Reads a project that matches the search parameters

        :param connection:      Database connection
        :param short_name:      Projects's short name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object

        NOTE:   This method only searches active projects
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(connection,
                                                                                   "short_name",
                                                                                   short_name,
                                                                                   True,
                                                                                   max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = projects[0]

        return project

    @staticmethod
    def __read_project_by_full_name(connection: Connection,
                                    full_name: str,
                                    max_revision_id: int) -> Optional[dict]:
        """
        Reads a project that matches the search parameters

        :param connection:      Database connection
        :param full_name:       Projects's full name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object

        NOTE:   This method only searches active projects
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(connection,
                                                                                   "full_name",
                                                                                   full_name,
                                                                                   True,
                                                                                   max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = projects[0]

        return project

    @staticmethod
    def __create_project(connection: Connection,
                         short_name: str,
                         full_name: str,
                         description: str,
                         revision_id: int) -> Optional[int]:
        """
        Creates a new user

        :param connection:  Database connection
        :param short_name:  Project's short name
        :param full_name:   Project's full name
        :param description: Project's description
        :param revision_id: Revision ID

        :return:    Project ID of the newly created project
        """
        # Check if a user with the same user name already exists
        project = ProjectManagementInterface.__read_project_by_short_name(connection,
                                                                          short_name,
                                                                          revision_id)

        if project is not None:
            return None

        # Create the project in the new revision
        project_id = DatabaseInterface.tables().project.insert_row(connection)

        if project_id is None:
            return None

        # Add project information to the project
        project_information_id = DatabaseInterface.tables().user_information.insert_row(connection,
                                                                                        project_id,
                                                                                        short_name,
                                                                                        full_name,
                                                                                        description,
                                                                                        True,
                                                                                        revision_id)

        if project_information_id is None:
            return None

        return project_id
