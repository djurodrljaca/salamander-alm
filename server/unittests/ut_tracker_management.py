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
from trackermanagement.tracker_management import TrackerManagementInterface, TrackerSelection
import unittest


class TrackerInformation(unittest.TestCase):
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

    def create_tracker_test2(self, project_id: int):
        tracker_id = TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                               project_id,
                                                               "test2",
                                                               "Test 2",
                                                               "Test tracker 2")
        return tracker_id

    def test_read_all_tracker_ids(self):
        # Create trackers
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker1 = TrackerManagementInterface.read_tracker_by_id(tracker_id1)
        self.assertIsNotNone(tracker1)

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        # Check active trackers (latest revision)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Active)

        self.assertEqual(len(tracker_ids), 2)
        self.assertListEqual(tracker_ids, [tracker_id1, tracker_id2])

        # Check active trackers (revision from tracker2)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Active,
                                                                      tracker2["revision_id"])

        self.assertEqual(len(tracker_ids), 2)
        self.assertListEqual(tracker_ids, [tracker_id1, tracker_id2])

        # Check active trackers (revision from tracker1)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Active,
                                                                      tracker1["revision_id"])

        self.assertEqual(len(tracker_ids), 1)
        self.assertListEqual(tracker_ids, [tracker_id1])

        # Deactivate tracker
        self.assertTrue(TrackerManagementInterface.deactivate_tracker(self.__admin_user_id,
                                                                      tracker_id1))

        # Recheck active trackers (revision from tracker2)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Active,
                                                                      tracker2["revision_id"])

        self.assertEqual(len(tracker_ids), 2)
        self.assertListEqual(tracker_ids, [tracker_id1, tracker_id2])

        # Recheck active trackers (latest revision)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Active)

        self.assertEqual(len(tracker_ids), 1)
        self.assertListEqual(tracker_ids, [tracker_id2])

        # Check inactive trackers (latest revision)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Inactive)

        self.assertEqual(len(tracker_ids), 1)
        self.assertListEqual(tracker_ids, [tracker_id1])

        # Check inactive trackers (revision from tracker2)
        tracker_ids = TrackerManagementInterface.read_all_tracker_ids(project_id1,
                                                                      TrackerSelection.Inactive,
                                                                      tracker2["revision_id"])

        self.assertEqual(len(tracker_ids), 0)

    def test_read_tracker_by_id(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker1 = TrackerManagementInterface.read_tracker_by_id(tracker_id1)

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], True)
        self.assertIsNotNone(tracker1["revision_id"])

        self.assertIsNone(
            TrackerManagementInterface.read_tracker_by_id(tracker_id1,
                                                          tracker1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerManagementInterface.read_tracker_by_id(999))

    def test_read_tracker_by_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker1 = TrackerManagementInterface.read_tracker_by_short_name("test1")

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], True)
        self.assertIsNotNone(tracker1["revision_id"])

        self.assertIsNone(
            TrackerManagementInterface.read_tracker_by_short_name(tracker1["short_name"],
                                                                  tracker1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerManagementInterface.read_tracker_by_short_name(""))
        self.assertIsNone(TrackerManagementInterface.read_tracker_by_short_name("test999"))

    def test_read_trackers_by_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        self.assertTrue(TrackerManagementInterface.deactivate_tracker(self.__admin_user_id,
                                                                      tracker_id1))

        tracker_id2 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id2)

        # Positive tests ---------------------------------------------------------------------------
        trackers = TrackerManagementInterface.read_trackers_by_short_name("test1")
        self.assertEqual(len(trackers), 2)

        tracker1 = trackers[0]
        tracker2 = trackers[1]

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], False)
        self.assertIsNotNone(tracker1["revision_id"])

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test1")
        self.assertEqual(tracker2["full_name"], "Test 1")
        self.assertEqual(tracker2["description"], "Test tracker 1")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        trackers = TrackerManagementInterface.read_trackers_by_short_name(
            tracker2["short_name"],
            tracker2["revision_id"] - 1)
        self.assertEqual(len(trackers), 1)

        tracker1 = trackers[0]

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], False)
        self.assertIsNotNone(tracker1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(len(TrackerManagementInterface.read_trackers_by_short_name("")), 0)
        self.assertEqual(len(TrackerManagementInterface.read_trackers_by_short_name("test999")), 0)

    def test_read_tracker_by_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        # Positive tests ---------------------------------------------------------------------------
        tracker1 = TrackerManagementInterface.read_tracker_by_full_name("Test 1")

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], True)
        self.assertIsNotNone(tracker1["revision_id"])

        self.assertIsNone(
            TrackerManagementInterface.read_tracker_by_full_name(tracker1["full_name"],
                                                                 tracker1["revision_id"] - 1))

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(TrackerManagementInterface.read_tracker_by_full_name(""))
        self.assertIsNone(TrackerManagementInterface.read_tracker_by_full_name("Test XYZ"))

    def test_read_trackers_by_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        self.assertTrue(TrackerManagementInterface.deactivate_tracker(self.__admin_user_id,
                                                                      tracker_id1))

        tracker_id2 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id2)

        # Positive tests ---------------------------------------------------------------------------
        trackers = TrackerManagementInterface.read_trackers_by_full_name("Test 1")
        self.assertEqual(len(trackers), 2)

        tracker1 = trackers[0]
        tracker2 = trackers[1]

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], False)
        self.assertIsNotNone(tracker1["revision_id"])

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test1")
        self.assertEqual(tracker2["full_name"], "Test 1")
        self.assertEqual(tracker2["description"], "Test tracker 1")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        trackers = TrackerManagementInterface.read_trackers_by_full_name(
            tracker2["full_name"],
            tracker2["revision_id"] - 1)
        self.assertEqual(len(trackers), 1)

        tracker1 = trackers[0]

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], False)
        self.assertIsNotNone(tracker1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertEqual(len(TrackerManagementInterface.read_trackers_by_full_name("")), 0)
        self.assertEqual(len(TrackerManagementInterface.read_trackers_by_full_name("Test XYZ")), 0)

    def test_create_tracker(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(self.create_tracker_test1(project_id1))

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a tracker with a reference to a non-existing user
        self.assertIsNone(TrackerManagementInterface.create_tracker(999,
                                                                    project_id1,
                                                                    "test_other",
                                                                    "Test Other",
                                                                    "Other test tracker"))

        # Try to create a tracker with a reference to a non-existing project
        self.assertIsNone(TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                                    999,
                                                                    "test_other",
                                                                    "Test Other",
                                                                    "Other test tracker"))

        # Try to create a tracker with an invalid short name
        self.assertIsNone(TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                                    project_id1,
                                                                    "",
                                                                    "Test Other",
                                                                    "Other test tracker"))

        self.assertIsNone(TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                                    project_id1,
                                                                    "test1",
                                                                    "Test Other",
                                                                    "Other test tracker"))

        # Try to create a tracker with an invalid full name
        self.assertIsNone(TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                                    project_id1,
                                                                    "test_other",
                                                                    "",
                                                                    "Other test tracker"))

        self.assertIsNone(TrackerManagementInterface.create_tracker(self.__admin_user_id,
                                                                    project_id1,
                                                                    "test_other",
                                                                    "Test 1",
                                                                    "Other test tracker"))

    def test_update_tracker_invalid_tracker_id(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Try to update a tracker with a reference to a non-existing tracker ID
        self.assertFalse(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            999,
            tracker2["short_name"],
            tracker2["full_name"],
            tracker2["description"],
            tracker2["active"]))

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_tracker_short_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker1 = TrackerManagementInterface.read_tracker_by_id(tracker_id1)
        self.assertIsNotNone(tracker1)

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], True)
        self.assertIsNotNone(tracker1["revision_id"])

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            "test_other",
            tracker2["full_name"],
            tracker2["description"],
            tracker2["active"]))

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test_other")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            "",
            tracker2["full_name"],
            tracker2["description"],
            tracker2["active"]))

        self.assertFalse(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            tracker1["short_name"],
            tracker2["full_name"],
            tracker2["description"],
            tracker2["active"]))

    def test_update_tracker_full_name(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id1 = self.create_tracker_test1(project_id1)
        self.assertIsNotNone(tracker_id1)

        tracker1 = TrackerManagementInterface.read_tracker_by_id(tracker_id1)
        self.assertIsNotNone(tracker1)

        self.assertEqual(tracker1["id"], tracker_id1)
        self.assertEqual(tracker1["project_id"], project_id1)
        self.assertEqual(tracker1["short_name"], "test1")
        self.assertEqual(tracker1["full_name"], "Test 1")
        self.assertEqual(tracker1["description"], "Test tracker 1")
        self.assertEqual(tracker1["active"], True)
        self.assertIsNotNone(tracker1["revision_id"])

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            tracker2["short_name"],
            "Test Other",
            tracker2["description"],
            tracker2["active"]))

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test Other")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            tracker2["short_name"],
            "",
            tracker2["description"],
            tracker2["active"]))

        self.assertFalse(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            tracker2["short_name"],
            tracker1["full_name"],
            tracker2["description"],
            tracker2["active"]))

    def test_update_tracker_description(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(TrackerManagementInterface.update_tracker_information(
            self.__admin_user_id,
            tracker_id2,
            tracker2["short_name"],
            tracker2["full_name"],
            "Test tracker other",
            tracker2["active"]))

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)
        self.assertIsNotNone(tracker2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker other")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_deactivate_activate_tracker(self):
        project_id1 = self.create_project_test1()
        self.assertIsNotNone(project_id1)

        tracker_id2 = self.create_tracker_test2(project_id1)
        self.assertIsNotNone(tracker_id2)

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Deactivate tracker
        self.assertTrue(TrackerManagementInterface.deactivate_tracker(self.__admin_user_id,
                                                                      tracker_id2))

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], False)
        self.assertIsNotNone(tracker2["revision_id"])

        # Activate tracker
        self.assertTrue(TrackerManagementInterface.activate_tracker(self.__admin_user_id,
                                                                    tracker_id2))

        tracker2 = TrackerManagementInterface.read_tracker_by_id(tracker_id2)

        self.assertEqual(tracker2["id"], tracker_id2)
        self.assertEqual(tracker2["project_id"], project_id1)
        self.assertEqual(tracker2["short_name"], "test2")
        self.assertEqual(tracker2["full_name"], "Test 2")
        self.assertEqual(tracker2["description"], "Test tracker 2")
        self.assertEqual(tracker2["active"], True)
        self.assertIsNotNone(tracker2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

if __name__ == '__main__':
    unittest.main()
