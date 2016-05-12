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
from database.tables.project_information import ProjectSelection
import datetime
from typing import List, Optional


class ProjectManagementInterface(object):
    """
    Project management

    Dependencies:

    - DatabaseInterface
    """

    def __init__(self):
        """
        Constructor is disabled!
        """
        raise RuntimeError()

    @staticmethod
    def read_all_project_ids(project_selection=ProjectSelection.Active,
                             max_revision_id=None) -> List[int]:
        """
        Reads all project IDs from the database

        :param project_selection:   Search for active, inactive or all project
        :param max_revision_id:     Maximum revision ID for the search ("None" for latest revision)

        :return:    List of project IDs
        """
        connection = DatabaseInterface.create_connection()

        if max_revision_id is None:
            max_revision_id = DatabaseInterface.tables().revision.read_current_revision_id(
                connection)

        # Reads all project IDs from the database
        projects = None

        if max_revision_id is not None:
            projects = DatabaseInterface.tables().project_information.read_all_project_ids(
                connection,
                project_selection,
                max_revision_id)

        return projects

    @staticmethod
    def read_project_by_id(project_id: int, max_revision_id=None) -> Optional[dict]:
        """
        Reads a project (active or inactive) that matches the specified project ID

        :param project_id:      ID of the project
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Project information object

        Returned dictionary contains items:

        - id
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

        # Read a project that matches the specified project ID
        project = None

        if max_revision_id is not None:
            project = ProjectManagementInterface.__read_project_by_id(connection,
                                                                      project_id,
                                                                      max_revision_id)

        return project

    @staticmethod
    def read_project_by_short_name(short_name: str, max_revision_id=None) -> Optional[dict]:
        """
        Reads an active project that matches the specified short name

        :param short_name:      Project's short name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Project information object

        Returned dictionary contains items:

        - id
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

        # Read a project that matches the specified short name
        project = None

        if max_revision_id is not None:
            project = ProjectManagementInterface.__read_project_by_short_name(connection,
                                                                              short_name,
                                                                              max_revision_id)

        return project

    @staticmethod
    def read_projects_by_short_name(short_name: str, max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive projects that match the specified short name

        :param short_name:      Project's short name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Project information of all projects that match the search attribute

        Each dictionary in the returned list contains items:

        - id
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

        # Read projects that match the specified short name
        projects = list()

        if max_revision_id is not None:
            project_information_list = \
                DatabaseInterface.tables().project_information.read_information(
                    connection,
                    "short_name",
                    short_name,
                    ProjectSelection.All,
                    max_revision_id)

            for project_information in project_information_list:
                projects.append(ProjectManagementInterface.__parse_project_information(
                    project_information))

        return projects

    @staticmethod
    def read_project_by_full_name(full_name: str, max_revision_id=None) -> Optional[dict]:
        """
        Reads an active project that matches the specified full name

        :param full_name:       Project's full name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Project information object

        Returned dictionary contains items:

        - id
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

        # Read a project that matches the specified full name
        project = None

        if max_revision_id is not None:
            project = ProjectManagementInterface.__read_project_by_full_name(connection,
                                                                             full_name,
                                                                             max_revision_id)

        return project

    @staticmethod
    def read_projects_by_full_name(full_name: str, max_revision_id=None) -> List[dict]:
        """
        Reads all active and inactive projects that match the specified short name

        :param full_name:       Projects's full name
        :param max_revision_id: Maximum revision ID for the search ("None" for latest revision)

        :return:    Project information of all projects that match the search attribute

        Each dictionary in the returned list contains items:

        - id
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

        # Read projects that match the specified full name
        projects = list()

        if max_revision_id is not None:
            project_information_list = \
                DatabaseInterface.tables().project_information.read_information(
                    connection,
                    "full_name",
                    full_name,
                    ProjectSelection.All,
                    max_revision_id)

            for project_information in project_information_list:
                projects.append(ProjectManagementInterface.__parse_project_information(
                    project_information))

        return projects

    @staticmethod
    def create_project(requested_by_user: int,
                       short_name: str,
                       full_name: str,
                       description: str) -> Optional[int]:
        """
        Creates a new project

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
        Updates project's information

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
                    if project["id"] != project_to_modify:
                        success = False

            # Check if there is already an existing project with the same full name
            if success:
                project = ProjectManagementInterface.__read_project_by_full_name(connection,
                                                                                 full_name,
                                                                                 revision_id)

                if project is not None:
                    if project["id"] != project_to_modify:
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
    def activate_project(requested_by_user: int, project_id: int) -> bool:
        """
        Activates an inactive project

        :param requested_by_user:   ID of the user that requested modification of the user
        :param project_id:  ID of the project that should be activated

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

            # Read project
            project = None

            if success:
                project = ProjectManagementInterface.__read_project_by_id(connection,
                                                                          project_id,
                                                                          revision_id)

                if project is None:
                    success = False
                elif project["active"]:
                    # Error, project is already active
                    success = False

            # Activate project
            if success:
                success = DatabaseInterface.tables().project_information.insert_row(
                    connection,
                    project_id,
                    project["short_name"],
                    project["full_name"],
                    project["description"],
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
    def deactivate_project(requested_by_user: int, project_id: int) -> bool:
        """
        Deactivates an active project

        :param requested_by_user:   ID of the user that requested modification of the user
        :param project_id: ID of the project that should be deactivated

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

            # Read project
            project = None

            if success:
                project = ProjectManagementInterface.__read_project_by_id(connection,
                                                                          project_id,
                                                                          revision_id)

                if project is None:
                    success = False
                elif not project["active"]:
                    # Error, project is already inactive
                    success = False

            # Deactivate project
            if success:
                success = DatabaseInterface.tables().project_information.insert_row(
                    connection,
                    project_id,
                    project["short_name"],
                    project["full_name"],
                    project["description"],
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
    def __read_project_by_id(connection: Connection,
                             project_id: int,
                             max_revision_id: int) -> Optional[dict]:
        """
        Reads a project (active or inactive) that matches the search parameters

        :param connection:      Database connection
        :param project_id:      ID of the project
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object

        Returned dictionary contains items:

        - id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(
            connection,
            "project_id",
            project_id,
            ProjectSelection.All,
            max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = {"id": projects[0]["project_id"],
                           "short_name": projects[0]["short_name"],
                           "full_name": projects[0]["full_name"],
                           "description": projects[0]["description"],
                           "active": projects[0]["active"],
                           "revision_id": projects[0]["revision_id"]}

        return project

    @staticmethod
    def __read_project_by_short_name(connection: Connection,
                                     short_name: str,
                                     max_revision_id: int) -> Optional[dict]:
        """
        Reads an active project that matches the specified short name

        :param connection:      Database connection
        :param short_name:      Projects's short name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object

        Returned dictionary contains items:

        - id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(
            connection,
            "short_name",
            short_name,
            ProjectSelection.Active,
            max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = {"id": projects[0]["project_id"],
                           "short_name": projects[0]["short_name"],
                           "full_name": projects[0]["full_name"],
                           "description": projects[0]["description"],
                           "active": projects[0]["active"],
                           "revision_id": projects[0]["revision_id"]}

        return project

    @staticmethod
    def __read_project_by_full_name(connection: Connection,
                                    full_name: str,
                                    max_revision_id: int) -> Optional[dict]:
        """
        Reads an active project that matches the specified full name

        :param connection:      Database connection
        :param full_name:       Projects's full name
        :param max_revision_id: Maximum revision ID for the search

        :return:    Project information object

        Returned dictionary contains items:

        - id
        - short_name
        - full_name
        - description
        - active
        - revision_id
        """
        # Read the projects that match the search attribute
        projects = DatabaseInterface.tables().project_information.read_information(
            connection,
            "full_name",
            full_name,
            ProjectSelection.Active,
            max_revision_id)

        # Return a project only if exactly one was found
        project = None

        if projects is not None:
            if len(projects) == 1:
                project = {"id": projects[0]["project_id"],
                           "short_name": projects[0]["short_name"],
                           "full_name": projects[0]["full_name"],
                           "description": projects[0]["description"],
                           "active": projects[0]["active"],
                           "revision_id": projects[0]["revision_id"]}

        return project

    @staticmethod
    def __create_project(connection: Connection,
                         short_name: str,
                         full_name: str,
                         description: str,
                         revision_id: int) -> Optional[int]:
        """
        Creates a new project

        :param connection:  Database connection
        :param short_name:  Project's short name
        :param full_name:   Project's full name
        :param description: Project's description
        :param revision_id: Revision ID

        :return:    Project ID of the newly created project
        """
        # Check if a project with the same short name already exists
        project = ProjectManagementInterface.__read_project_by_short_name(connection,
                                                                          short_name,
                                                                          revision_id)

        if project is not None:
            return None

        # Check if a project with the same full name already exists
        project = ProjectManagementInterface.__read_project_by_full_name(connection,
                                                                         full_name,
                                                                         revision_id)

        if project is not None:
            return None

        # Create the project in the new revision
        project_id = DatabaseInterface.tables().project.insert_row(connection)

        if project_id is None:
            return None

        # Add project information to the project
        project_information_id = DatabaseInterface.tables().project_information.insert_row(
            connection,
            project_id,
            short_name,
            full_name,
            description,
            True,
            revision_id)

        if project_information_id is None:
            return None

        return project_id

    @staticmethod
    def __parse_project_information(project_information: dict) -> dict:
        return {"id": project_information["project_id"],
                "short_name": project_information["short_name"],
                "full_name": project_information["full_name"],
                "description": project_information["description"],
                "active": project_information["active"],
                "revision_id": project_information["revision_id"]}
