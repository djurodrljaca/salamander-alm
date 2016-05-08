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

import os
import plugins.database.sqlite.database
import plugins.authentication.basic.authentication_method
import unittest
import usermanagement.user_management


def _create_database():
    database_file_path = "database.db"
    if os.path.exists(database_file_path):
        os.remove(database_file_path)

    database_object = plugins.database.sqlite.database.DatabaseSqlite(database_file_path)

    if not database_object.create_new_database():
        database_object = None

    return database_object


class UserInformation(unittest.TestCase):
    def setUp(self):
        self.__database = _create_database()
        self.__user_management = usermanagement.user_management.UserManagement(self.__database)
        self.__user_management.add_authentication_method(
            plugins.authentication.basic.authentication_method.AuthenticationMethodBasic())
        self.__admin_user_id = 1

    def create_user_test1(self):
        user_id = self.__user_management.create_user(self.__admin_user_id,
                                                     "test1",
                                                     "Test",
                                                     "test1@test.com",
                                                     "basic",
                                                     {"password": "test123"})
        return user_id

    def create_user_test2(self):
        user_id = self.__user_management.create_user(self.__admin_user_id,
                                                     "test2",
                                                     "Test",
                                                     "test2@test.com",
                                                     "basic",
                                                     {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        user = self.__user_management.read_user_by_user_id(self.__admin_user_id)

        self.assertIsNotNone(user)
        self.assertEqual(user["user_id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)
        self.assertIsNotNone(user["revision_id"])

    def test_create_user(self):
        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(self.create_user_test1())

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a user with a reference to a non-existing user
        self.assertIsNone(self.__user_management.create_user(None,
                                                             "test_other",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        self.assertIsNone(self.__user_management.create_user(999,
                                                             "test_other",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        # Try to create a user with an invalid user name
        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             None,
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        # Try to create a user with the same user name as another user
        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "test1",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        # Try to create a user with an invalid display name
        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "test_other",
                                                             None,
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "test_other",
                                                             "",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"}))

        # Try to create a user with an invalid authentication type
        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "test_other",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             None,
                                                             {"password": "test123"}))

        self.assertIsNone(self.__user_management.create_user(self.__admin_user_id,
                                                             "test_other",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "",
                                                             {"password": "test123"}))

    def test_read_user_by_user_id(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = self.__user_management.read_user_by_user_id(user_id)

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)
        self.assertIsNotNone(user["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(self.__user_management.read_user_by_user_id(None))
        self.assertIsNone(self.__user_management.read_user_by_user_id(999))

    def test_read_user_by_user_name(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = self.__user_management.read_user_by_user_name("test1")

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)
        self.assertIsNotNone(user["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(self.__user_management.read_user_by_user_name(None))
        self.assertIsNone(self.__user_management.read_user_by_user_name(""))
        self.assertIsNone(self.__user_management.read_user_by_user_name("test999"))

    def test_reads_user_by_user_name(self):
        # Create a user and then deactivate it and create a user with the same user name
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = self.__user_management.read_user_by_user_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(self.__user_management.update_user_information(self.__admin_user_id,
                                                                       user_id1,
                                                                       user1["user_name"],
                                                                       user1["display_name"],
                                                                       user1["email"],
                                                                       False))

        user_id2 = self.create_user_test1()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        # Only active users
        users = self.__user_management.read_users_by_user_name("test1", True)
        self.assertEqual(len(users), 1)

        user2 = users[0]

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test1")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test1@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Both active and inactive users
        users = self.__user_management.read_users_by_user_name("test1", False)
        self.assertEqual(len(users), 2)

        if ((users[0]["user_id"] == user_id1) and
                (users[1]["user_id"] == user_id2)):
            user1 = users[0]
            user2 = users[1]
        elif ((users[1]["user_id"] == user_id1) and
                  (users[0]["user_id"] == user_id2)):
            user1 = users[1]
            user2 = users[0]
        else:
            self.fail("Invalid user IDs")

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], False)
        self.assertIsNotNone(user1["revision_id"])

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test1")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test1@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        users = self.__user_management.read_users_by_user_name(None, False)
        self.assertEqual(len(users), 0)

        users = self.__user_management.read_users_by_user_name("", False)
        self.assertEqual(len(users), 0)

        users = self.__user_management.read_users_by_user_name("test999", False)
        self.assertEqual(len(users), 0)

    def test_read_users_by_display_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = self.__user_management.read_user_by_user_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(self.__user_management.update_user_information(self.__admin_user_id,
                                                                       user_id1,
                                                                       user1["user_name"],
                                                                       user1["display_name"],
                                                                       user1["email"],
                                                                       False))

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        # Only active users
        users = self.__user_management.read_users_by_display_name("Test", True)
        self.assertEqual(len(users), 1)

        user2 = users[0]

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Both active and inactive users
        users = self.__user_management.read_users_by_display_name("Test", False)
        self.assertEqual(len(users), 2)

        if ((users[0]["user_id"] == user_id1) and
                (users[1]["user_id"] == user_id2)):
            user1 = users[0]
            user2 = users[1]
        elif ((users[1]["user_id"] == user_id1) and
                  (users[0]["user_id"] == user_id2)):
            user1 = users[1]
            user2 = users[0]
        else:
            self.fail("Invalid user IDs")

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], False)
        self.assertIsNotNone(user1["revision_id"])

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        users = self.__user_management.read_users_by_display_name(None)
        self.assertEqual(len(users), 0)

        users = self.__user_management.read_users_by_display_name("")
        self.assertEqual(len(users), 0)

        users = self.__user_management.read_users_by_display_name("Test XYZ")
        self.assertEqual(len(users), 0)

    def test_update_user_invalid_ids(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Try to update a user with a reference to a non-existing "requested by user"
        self.assertFalse(self.__user_management.update_user_information(None,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

        self.assertFalse(self.__user_management.update_user_information(999,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

        # Try to update a user with a reference to a non-existing user ID
        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        None,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        999,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

    def test_update_user_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = self.__user_management.read_user_by_user_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)
        self.assertIsNotNone(user1["revision_id"])

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(self.__user_management.update_user_information(user_id1,
                                                                       user_id1,
                                                                       "test1new",
                                                                       user1["display_name"],
                                                                       user1["email"],
                                                                       user1["active"]))

        user1 = self.__user_management.read_user_by_user_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1new")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)
        self.assertIsNotNone(user1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid user name
        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        user_id2,
                                                                        None,
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        user_id2,
                                                                        "",
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

        # Try to update a user with the same user name as another user
        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        user_id2,
                                                                        user1["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        user2["active"]))

    def test_update_display_name(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(self.__user_management.update_user_information(user_id2,
                                                                       user_id2,
                                                                       user2["user_name"],
                                                                       "Test New",
                                                                       user2["email"],
                                                                       user2["active"]))

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test New")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid display name
        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        None,
                                                                        user2["email"],
                                                                        user2["active"]))

        self.assertFalse(self.__user_management.update_user_information(self.__admin_user_id,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        "",
                                                                        user2["email"],
                                                                        user2["active"]))

    def test_update_email(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(self.__user_management.update_user_information(user_id2,
                                                                       user_id2,
                                                                       user2["user_name"],
                                                                       user2["display_name"],
                                                                       "test2new@test.com",
                                                                       user2["active"]))

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2new@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_disable_enable_user(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Disable user
        self.assertTrue(self.__user_management.update_user_information(user_id2,
                                                                       user_id2,
                                                                       user2["user_name"],
                                                                       user2["display_name"],
                                                                       user2["email"],
                                                                       False))

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], False)
        self.assertIsNotNone(user2["revision_id"])

        # Enable user
        self.assertTrue(self.__user_management.update_user_information(user_id2,
                                                                       user_id2,
                                                                       user2["user_name"],
                                                                       user2["display_name"],
                                                                       user2["email"],
                                                                       True))

        user2 = self.__user_management.read_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(self.__user_management.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        None))

        self.assertFalse(self.__user_management.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        -1))

        self.assertFalse(self.__user_management.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        2))

    # TODO: add test for: find_user_information_history


class UserAuthentication(unittest.TestCase):
    def setUp(self):
        self.__database = _create_database()
        self.__user_management = usermanagement.user_management.UserManagement(self.__database)
        self.__user_management.add_authentication_method(
            plugins.authentication.basic.authentication_method.AuthenticationMethodBasic())
        self.__admin_user_id = 1

    def create_user_test1(self):
        user_id = self.__user_management.create_user(self.__admin_user_id,
                                                     "test1",
                                                     "Test",
                                                     "test1@test.com",
                                                     "basic",
                                                     {"password": "test123"})
        return user_id

    def create_user_test2(self):
        user_id = self.__user_management.create_user(self.__admin_user_id,
                                                     "test2",
                                                     "Test",
                                                     "test2@test.com",
                                                     "basic",
                                                     {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        self.assertTrue(self.__user_management.authenticate_user("administrator",
                                                                 {"password": "administrator"}))

    def test_users(self):
        self.assertIsNotNone(self.create_user_test1())
        self.assertIsNotNone(self.create_user_test2())

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(self.__user_management.authenticate_user("test1",
                                                                 {"password": "test123"}))

        self.assertTrue(self.__user_management.authenticate_user("test2",
                                                                 {"password": "test456"}))

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(self.__user_management.authenticate_user(None,
                                                                  {"password": "test123"}))

        self.assertFalse(self.__user_management.authenticate_user("",
                                                                  {"password": "test456"}))

        self.assertFalse(self.__user_management.authenticate_user("test1",
                                                                  {"password": "Test123"}))

        self.assertFalse(self.__user_management.authenticate_user("test1",
                                                                  {"password": "test456"}))

        self.assertFalse(self.__user_management.authenticate_user("test1",
                                                                  {"password": ""}))

        self.assertFalse(self.__user_management.authenticate_user("test2",
                                                                  {"password": "tEst456"}))

        self.assertFalse(self.__user_management.authenticate_user("test2",
                                                                  {"password": "test123"}))

    def test_basic_update_update_password(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        self.assertTrue(self.__user_management.authenticate_user("test1",
                                                                 {"password": "test123"}))

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(self.__user_management.update_user_authentication(user_id1,
                                                                          "basic",
                                                                          {"password": "new_pw"}))

        user1 = self.__user_management.read_user_by_user_id(user_id1)

        self.assertTrue(self.__user_management.authenticate_user("test1",
                                                                 {"password": "new_pw"}))

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(self.__user_management.authenticate_user("test1",
                                                                  {"password": "test123"}))

    # TODO: add test for: read_user_authentication_history?
    # TODO: add test for: others...

if __name__ == '__main__':
    unittest.main()
