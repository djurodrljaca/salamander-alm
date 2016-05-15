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
from projectmanagement.project_management import ProjectManagementInterface
from trackermanagement.tracker_management import TrackerManagementInterface
from trackermanagement.tracker_field_management import \
    TrackerFieldManagementInterface, TrackerFieldSelection
import unittest


class TrackerFieldInformation(unittest.TestCase):
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

    def create_tracker_test1(self, project_id: int):
        tracker_id = TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                               project_id,
                                                               "test1",
                                                               "Test 1",
                                                               "Test tracker 1")
        return tracker_id

    def create_tracker_field_test1(self, tracker_id: int):
        tracker_field_id = TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id,
            "test1",
            "Test 1",
            "Test tracker field 1",
            "artifact_id",
            True)
        return tracker_field_id

    def create_tracker_field_test2(self, tracker_id: int):
        tracker_field_id = TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id,
            "test2",
            "Test 2",
            "Test tracker field 2",
            "artifact_id",
            False)
        return tracker_field_id

    def test_read_all_tracker_field_ids(self):
        # Create tracker fields
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id1)
        self.assertIsNotNone(tracker_field1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        # Check active tracker fields (latest revision)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Active)

        self.assertEqual(len(tracker_field_ids), 2)
        self.assertListEqual(tracker_field_ids, [tracker_field_id1, tracker_field_id2])

        # Check active tracker fields (revision from tracker_field2)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Active,
            tracker_field2["revision_id"])

        self.assertEqual(len(tracker_field_ids), 2)
        self.assertListEqual(tracker_field_ids, [tracker_field_id1, tracker_field_id2])

        # Check active tracker fields (revision from tracker_field1)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Active,
            tracker_field1["revision_id"])

        self.assertEqual(len(tracker_field_ids), 1)
        self.assertListEqual(tracker_field_ids, [tracker_field_id1])

        # Deactivate tracker field
        self.assertTrue(TrackerFieldManagementInterface.deactivate_tracker_field(
            self.__admin_user_id,
            tracker_field_id1))

        # Recheck active tracker fields (revision from tracker2)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Active,
            tracker_field2["revision_id"])

        self.assertEqual(len(tracker_field_ids), 2)
        self.assertListEqual(tracker_field_ids, [tracker_field_id1, tracker_field_id2])

        # Recheck active tracker fields (latest revision)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Active)

        self.assertEqual(len(tracker_field_ids), 1)
        self.assertListEqual(tracker_field_ids, [tracker_field_id2])

        # Check inactive tracker fields (latest revision)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Inactive)

        self.assertEqual(len(tracker_field_ids), 1)
        self.assertListEqual(tracker_field_ids, [tracker_field_id1])

        # Check inactive tracker fields (revision from tracker_field2)
        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(
            tracker_id1,
            TrackerFieldSelection.Inactive,
            tracker_field2["revision_id"])

        self.assertEqual(len(tracker_field_ids), 0)

    def test_read_tracker_field_by_id(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id1)

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        self.assertIsNone(
            TrackerFieldManagementInterface.read_tracker_field_by_id(
                tracker_field_id1,
                tracker_field1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerFieldManagementInterface.read_tracker_field_by_id(999))

    def test_read_tracker_field_by_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_name("test1")

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        self.assertIsNone(
            TrackerFieldManagementInterface.read_tracker_field_by_name(
                tracker_field1["name"],
                tracker_field1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerFieldManagementInterface.read_tracker_field_by_name(""))
        self.assertIsNone(TrackerFieldManagementInterface.read_tracker_field_by_name("test999"))

    def test_read_tracker_fields_by_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        self.assertTrue(TrackerFieldManagementInterface.deactivate_tracker_field(
            self.__admin_user_id,
            tracker_field_id1))

        tracker_field_id2 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        # Positive tests ---------------------------------------------------------------------------
        tracker_fields = TrackerFieldManagementInterface.read_tracker_fields_by_name("test1")
        self.assertEqual(len(tracker_fields), 2)

        tracker_field1 = tracker_fields[0]
        tracker_field2 = tracker_fields[1]

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], False)
        self.assertIsNotNone(tracker_field1["revision_id"])

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test1")
        self.assertEqual(tracker_field2["display_name"], "Test 1")
        self.assertEqual(tracker_field2["description"], "Test tracker field 1")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], True)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        tracker_fields = TrackerFieldManagementInterface.read_tracker_fields_by_name(
            tracker_field2["name"],
            tracker_field2["revision_id"] - 1)
        self.assertEqual(len(tracker_fields), 1)

        tracker_field1 = tracker_fields[0]

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], False)
        self.assertIsNotNone(tracker_field1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(len(TrackerFieldManagementInterface.read_tracker_fields_by_name("")), 0)
        self.assertEqual(
            len(TrackerFieldManagementInterface.read_tracker_fields_by_name("test999")), 0)

    def test_read_tracker_field_by_display_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker_field1 = \
            TrackerFieldManagementInterface.read_tracker_field_by_display_name("Test 1")

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        self.assertIsNone(
            TrackerFieldManagementInterface.read_tracker_field_by_display_name(
                tracker_field1["display_name"],
                tracker_field1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerFieldManagementInterface.read_tracker_field_by_display_name(""))
        self.assertIsNone(
            TrackerFieldManagementInterface.read_tracker_field_by_display_name("Test XYZ"))

    def test_read_tracker_fields_by_display_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        self.assertTrue(TrackerFieldManagementInterface.deactivate_tracker_field(
            self.__admin_user_id,
            tracker_field_id1))

        tracker_field_id2 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        # Positive tests ---------------------------------------------------------------------------
        tracker_fields = \
            TrackerFieldManagementInterface.read_tracker_fields_by_display_name("Test 1")
        self.assertEqual(len(tracker_fields), 2)

        tracker_field1 = tracker_fields[0]
        tracker_field2 = tracker_fields[1]

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], False)
        self.assertIsNotNone(tracker_field1["revision_id"])

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test1")
        self.assertEqual(tracker_field2["display_name"], "Test 1")
        self.assertEqual(tracker_field2["description"], "Test tracker field 1")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], True)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        tracker_fields = TrackerFieldManagementInterface.read_tracker_fields_by_display_name(
            tracker_field2["display_name"],
            tracker_field2["revision_id"] - 1)
        self.assertEqual(len(tracker_fields), 1)

        tracker_field1 = tracker_fields[0]

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], False)
        self.assertIsNotNone(tracker_field1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(
            len(TrackerFieldManagementInterface.read_tracker_fields_by_display_name("")), 0)
        self.assertEqual(
            len(TrackerFieldManagementInterface.read_tracker_fields_by_display_name("Test XYZ")), 0)

    def test_create_tracker_field(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(self.create_tracker_field_test1(tracker_id1))

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a tracker field with a reference to a non-existing user
        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            999,
            tracker_id1,
            "test_other",
            "Test Other",
            "Other test tracker field",
            "artifact_id",
            True))

        # Try to create a tracker field with a reference to a non-existing tracker
        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            999,
            "test_other",
            "Test Other",
            "Other test tracker field",
            "artifact_id",
            True))

        # Try to create a tracker field with an invalid name
        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id1,
            "",
            "Test Other",
            "Other test tracker field",
            "artifact_id",
            True))

        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id1,
            "test1",
            "Test Other",
            "Other test tracker field",
            "artifact_id",
            True))

        # Try to create a tracker field with an invalid display name
        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id1,
            "test_other",
            "",
            "Other test tracker field",
            "artifact_id",
            True))

        self.assertIsNone(TrackerFieldManagementInterface.create_tracker_field(
            self.__admin_user_id,
            tracker_id1,
            "test_other",
            "Test 1",
            "Other test tracker field",
            "artifact_id",
            True))

    def test_create_tracker_fields(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        self.assertTrue(TrackerFieldManagementInterface.create_tracker_fields(
            self.__admin_user_id,
            tracker_id1,
            [{"name": "test1",
              "display_name": "Test 1",
              "description": "Test tracker field 1",
              "field_type": "artifact_id",
              "required": True},
             {"name": "test2",
              "display_name": "Test 2",
              "description": "Test tracker field 2",
              "field_type": "artifact_id",
              "required": False}
             ]))

        tracker_field_ids = TrackerFieldManagementInterface.read_all_tracker_field_ids(tracker_id1)
        self.assertEqual(len(tracker_field_ids), 2)

        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_id(
            tracker_field_ids[0])

        self.assertEqual(tracker_field1["id"], tracker_field_ids[0])
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(
            tracker_field_ids[1])

        self.assertEqual(tracker_field2["id"], tracker_field_ids[1])
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

    def test_update_tracker_field_invalid_tracker_field_id(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Try to update a tracker field with a reference to a non-existing tracker field ID
        self.assertFalse(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            999,
            tracker_field2["name"],
            tracker_field2["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_tracker_field_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id1)
        self.assertIsNotNone(tracker_field1)

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            "test_other",
            tracker_field2["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test_other")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            "",
            tracker_field2["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        self.assertFalse(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field1["name"],
            tracker_field2["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

    def test_update_tracker_field_display_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id1 = self.create_tracker_field_test1(tracker_id1)
        self.assertIsNotNone(tracker_field_id1)

        tracker_field1 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id1)
        self.assertIsNotNone(tracker_field1)

        self.assertEqual(tracker_field1["id"], tracker_field_id1)
        self.assertEqual(tracker_field1["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field1["name"], "test1")
        self.assertEqual(tracker_field1["display_name"], "Test 1")
        self.assertEqual(tracker_field1["description"], "Test tracker field 1")
        self.assertEqual(tracker_field1["field_type"], "artifact_id")
        self.assertEqual(tracker_field1["required"], True)
        self.assertEqual(tracker_field1["active"], True)
        self.assertIsNotNone(tracker_field1["revision_id"])

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            "Test other",
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test other")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            "",
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        self.assertFalse(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            tracker_field1["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

    def test_update_tracker_field_description(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            tracker_field2["display_name"],
            "Test tracker field other",
            tracker_field2["field_type"],
            tracker_field2["required"],
            tracker_field2["active"]))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field other")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_tracker_field_type(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            tracker_field2["display_name"],
            tracker_field2["description"],
            "text_area",
            tracker_field2["required"],
            tracker_field2["active"]))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "text_area")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_tracker_field_required(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerFieldManagementInterface.update_tracker_field_information(
            self.__admin_user_id,
            tracker_field_id2,
            tracker_field2["name"],
            tracker_field2["display_name"],
            tracker_field2["description"],
            tracker_field2["field_type"],
            True,
            tracker_field2["active"]))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], True)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_deactivate_activate_tracker_field(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker_field_id2 = self.create_tracker_field_test2(tracker_id1)
        self.assertIsNotNone(tracker_field_id2)

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)
        self.assertIsNotNone(tracker_field2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Deactivate tracker field
        self.assertTrue(TrackerFieldManagementInterface.deactivate_tracker_field(
            self.__admin_user_id,
            tracker_field_id2))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], False)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Activate tracker
        self.assertTrue(TrackerFieldManagementInterface.activate_tracker_field(
            self.__admin_user_id,
            tracker_field_id2))

        tracker_field2 = TrackerFieldManagementInterface.read_tracker_field_by_id(tracker_field_id2)

        self.assertEqual(tracker_field2["id"], tracker_field_id2)
        self.assertEqual(tracker_field2["tracker_id"], tracker_id1)
        self.assertEqual(tracker_field2["name"], "test2")
        self.assertEqual(tracker_field2["display_name"], "Test 2")
        self.assertEqual(tracker_field2["description"], "Test tracker field 2")
        self.assertEqual(tracker_field2["field_type"], "artifact_id")
        self.assertEqual(tracker_field2["required"], False)
        self.assertEqual(tracker_field2["active"], True)
        self.assertIsNotNone(tracker_field2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

if __name__ == '__main__':
    unittest.main()
