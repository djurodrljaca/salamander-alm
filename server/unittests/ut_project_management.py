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

from authentication.authentication import AuthenticationInterface
from authentication.basic_authentication_method import AuthenticationMethodBasic
from database.database import DatabaseInterface
from plugins.database.sqlite.database import DatabaseSqlite
import unittest
from projectmanagement.project_management import ProjectManagementInterface


class ProjectInformation(unittest.TestCase):
    def setUp(self):
        # Authentication
        AuthenticationInterface.remove_all_authentication_methods()
        AuthenticationInterface.add_authentication_method(AuthenticationMethodBasic())

        # Database
        DatabaseInterface.load_database_plugin(DatabaseSqlite("database.db"))
        DatabaseInterface.create_new_database()

        # Data members
        self.__admin_user_id = 1

    def create_project_test1(self):
        project_id = ProjectManagementInterface.create_project(self.__admin_user_id,
                                                               "test1",
                                                               "Test 1",
                                                               "Test project 1")
        return project_id

    def create_project_test2(self):
        project_id = ProjectManagementInterface.create_project(self.__admin_user_id,
                                                               "test2",
                                                               "Test 2",
                                                               "Test project 2")
        return project_id

    def test_create_project(self):
        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(self.create_project_test1())

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a project with a reference to a non-existing user
        self.assertIsNone(ProjectManagementInterface.create_project(None,
                                                                    "test_other",
                                                                    "Test Other",
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(999,
                                                                    "test_other",
                                                                    "Test Other",
                                                                    "Other test project"))

        # Try to create a project with an invalid short name
        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    None,
                                                                    "Test Other",
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "",
                                                                    "Test Other",
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "test1",
                                                                    "Test Other",
                                                                    "Other test project"))

        # Try to create a project with an invalid full name
        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "test_other",
                                                                    None,
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "test_other",
                                                                    "",
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "test_other",
                                                                    "Test 1",
                                                                    "Other test project"))

    def test_read_all_project_ids(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project_ids = ProjectManagementInterface.read_all_project_ids()

        self.assertEqual(len(project_ids), 2)
        self.assertListEqual(project_ids, [project_id1, project_id2])

        self.assertNotEqual(project_id1, project_id2)

    # TODO: implement the other tests

if __name__ == '__main__':
    unittest.main()
