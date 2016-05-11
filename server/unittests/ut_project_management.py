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
from projectmanagement.project_management import ProjectManagementInterface, ProjectSelection
import unittest


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

    def test_read_all_user_ids(self):
        # Create projects
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        project1 = ProjectManagementInterface.read_project_by_id(project_id1)
        self.assertIsNotNone(project1)

        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        # Check active projects (latest revision)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Active)

        self.assertEqual(len(project_ids), 2)
        self.assertListEqual(project_ids, [project_id1, project_id2])

        # Check active projects (revision from project2)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Active,
                                                                      project2["revision_id"])

        self.assertEqual(len(project_ids), 2)
        self.assertListEqual(project_ids, [project_id1, project_id2])
        self.assertNotEqual(project_id1, project_id2)

        # Check active projects (revision from project1)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Active,
                                                                      project1["revision_id"])

        self.assertEqual(len(project_ids), 1)
        self.assertListEqual(project_ids, [project_id1])

        # Deactivate project
        self.assertTrue(ProjectManagementInterface.deactivate_project(self.__admin_user_id,
                                                                      project_id1))

        # Recheck active projects (revision from project2)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Active,
                                                                      project2["revision_id"])

        self.assertEqual(len(project_ids), 2)
        self.assertListEqual(project_ids, [project_id1, project_id2])
        self.assertNotEqual(project_id1, project_id2)

        # Recheck active projects (latest revision)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Active)

        self.assertEqual(len(project_ids), 1)
        self.assertListEqual(project_ids, [project_id2])

        # Check inactive projects (latest revision)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Inactive)

        self.assertEqual(len(project_ids), 1)
        self.assertListEqual(project_ids, [project_id1])

        # Check inactive projects (revision from project2)
        project_ids = ProjectManagementInterface.read_all_project_ids(ProjectSelection.Inactive,
                                                                      project2["revision_id"])

        self.assertEqual(len(project_ids), 0)

    def test_read_project_by_id(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        # Positive tests ---------------------------------------------------------------------------
        project1 = ProjectManagementInterface.read_project_by_id(project_id1)

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], True)
        self.assertIsNotNone(project1["revision_id"])

        self.assertIsNone(
            ProjectManagementInterface.read_project_by_id(project_id1,
                                                          project1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(ProjectManagementInterface.read_project_by_id(999))

    def test_read_project_by_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        # Positive tests ---------------------------------------------------------------------------
        project1 = ProjectManagementInterface.read_project_by_short_name("test1")

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], True)
        self.assertIsNotNone(project1["revision_id"])

        self.assertIsNone(
            ProjectManagementInterface.read_project_by_short_name(project1["short_name"],
                                                                  project1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(ProjectManagementInterface.read_project_by_short_name(""))
        self.assertIsNone(ProjectManagementInterface.read_project_by_short_name("test999"))

    def test_read_projects_by_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        self.assertTrue(ProjectManagementInterface.deactivate_project(self.__admin_user_id,
                                                                      project_id1))

        project_id2 = self.create_project_test1()
        self.assertIsNotNone(project_id2)

        # Positive tests ---------------------------------------------------------------------------
        projects = ProjectManagementInterface.read_projects_by_short_name("test1")
        self.assertEqual(len(projects), 2)

        project1 = projects[0]
        project2 = projects[1]

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], False)
        self.assertIsNotNone(project1["revision_id"])

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test1")
        self.assertEqual(project2["full_name"], "Test 1")
        self.assertEqual(project2["description"], "Test project 1")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        projects = ProjectManagementInterface.read_projects_by_short_name(
            project2["short_name"],
            project2["revision_id"] - 1)
        self.assertEqual(len(projects), 1)

        project1 = projects[0]

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], False)
        self.assertIsNotNone(project1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(len(ProjectManagementInterface.read_projects_by_short_name("")), 0)
        self.assertEqual(len(ProjectManagementInterface.read_projects_by_short_name("test999")), 0)

    def test_read_project_by_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        # Positive tests ---------------------------------------------------------------------------
        project1 = ProjectManagementInterface.read_project_by_full_name("Test 1")

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], True)
        self.assertIsNotNone(project1["revision_id"])

        self.assertIsNone(
            ProjectManagementInterface.read_project_by_full_name(project1["full_name"],
                                                                 project1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(ProjectManagementInterface.read_project_by_full_name(""))
        self.assertIsNone(ProjectManagementInterface.read_project_by_full_name("Test XYZ"))

    def test_read_projects_by_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        self.assertTrue(ProjectManagementInterface.deactivate_project(self.__admin_user_id,
                                                                      project_id1))

        project_id2 = self.create_project_test1()
        self.assertIsNotNone(project_id2)

        # Positive tests ---------------------------------------------------------------------------
        projects = ProjectManagementInterface.read_projects_by_full_name("Test 1")
        self.assertEqual(len(projects), 2)

        project1 = projects[0]
        project2 = projects[1]

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], False)
        self.assertIsNotNone(project1["revision_id"])

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test1")
        self.assertEqual(project2["full_name"], "Test 1")
        self.assertEqual(project2["description"], "Test project 1")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        projects = ProjectManagementInterface.read_projects_by_full_name(
            project2["full_name"],
            project2["revision_id"] - 1)
        self.assertEqual(len(projects), 1)

        project1 = projects[0]

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], False)
        self.assertIsNotNone(project1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(len(ProjectManagementInterface.read_projects_by_full_name("")), 0)
        self.assertEqual(len(ProjectManagementInterface.read_projects_by_full_name("Test XYZ")), 0)

    def test_create_project(self):
        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(self.create_project_test1())

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a project with a reference to a non-existing user
        self.assertIsNone(ProjectManagementInterface.create_project(999,
                                                                    "test_other",
                                                                    "Test Other",
                                                                    "Other test project"))

        # Try to create a project with an invalid short name
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
                                                                    "",
                                                                    "Other test project"))

        self.assertIsNone(ProjectManagementInterface.create_project(self.__admin_user_id,
                                                                    "test_other",
                                                                    "Test 1",
                                                                    "Other test project"))

    def test_update_project_invalid_project_id(self):
        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Try to update a project with a reference to a non-existing project ID
        self.assertFalse(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            999,
            project2["short_name"],
            project2["full_name"],
            project2["description"],
            project2["active"]))

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_project_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        project1 = ProjectManagementInterface.read_project_by_id(project_id1)
        self.assertIsNotNone(project1)

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], True)
        self.assertIsNotNone(project1["revision_id"])

        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            "test_other",
            project2["full_name"],
            project2["description"],
            project2["active"]))

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test_other")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            "",
            project2["full_name"],
            project2["description"],
            project2["active"]))

        self.assertFalse(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            project1["short_name"],
            project2["full_name"],
            project2["description"],
            project2["active"]))

    def test_update_project_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        project1 = ProjectManagementInterface.read_project_by_id(project_id1)
        self.assertIsNotNone(project1)

        self.assertEqual(project1["id"], project_id1)
        self.assertEqual(project1["short_name"], "test1")
        self.assertEqual(project1["full_name"], "Test 1")
        self.assertEqual(project1["description"], "Test project 1")
        self.assertEqual(project1["active"], True)
        self.assertIsNotNone(project1["revision_id"])

        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            project2["short_name"],
            "Test Other",
            project2["description"],
            project2["active"]))

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test Other")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            project2["short_name"],
            "",
            project2["description"],
            project2["active"]))

        self.assertFalse(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            project2["short_name"],
            project1["full_name"],
            project2["description"],
            project2["active"]))

    def test_update_project_description(self):
        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(ProjectManagementInterface.update_project_information(
            self.__admin_user_id,
            project_id2,
            project2["short_name"],
            project2["full_name"],
            "Test project other",
            project2["active"]))

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)
        self.assertIsNotNone(project2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project other")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_deactivate_activate_project(self):
        project_id2 = self.create_project_test2()
        self.assertIsNotNone(project_id2)

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Deactivate project
        self.assertTrue(ProjectManagementInterface.deactivate_project(self.__admin_user_id,
                                                                      project_id2))

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], False)
        self.assertIsNotNone(project2["revision_id"])

        # Activate project
        self.assertTrue(ProjectManagementInterface.activate_project(self.__admin_user_id,
                                                                    project_id2))

        project2 = ProjectManagementInterface.read_project_by_id(project_id2)

        self.assertEqual(project2["id"], project_id2)
        self.assertEqual(project2["short_name"], "test2")
        self.assertEqual(project2["full_name"], "Test 2")
        self.assertEqual(project2["description"], "Test project 2")
        self.assertEqual(project2["active"], True)
        self.assertIsNotNone(project2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

if __name__ == '__main__':
    unittest.main()
