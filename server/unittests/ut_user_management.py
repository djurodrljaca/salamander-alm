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
from usermanagement.user_management import UserManagementInterface


def _initialize_system():
    # Authentication
    AuthenticationInterface.remove_all_authentication_methods()
    AuthenticationInterface.add_authentication_method(AuthenticationMethodBasic())

    # Database
    database_file_path = "database.db"
    DatabaseInterface.load_database_plugin(DatabaseSqlite(database_file_path))

    # User management
    # No initialization needed


class UserInformation(unittest.TestCase):
    def setUp(self):
        _initialize_system()
        DatabaseInterface.create_new_database()
        self.__admin_user_id = 1

    def create_user_test1(self):
        user_id = UserManagementInterface.create_user(self.__admin_user_id,
                                                      "test1",
                                                      "Test",
                                                      "test1@test.com",
                                                      "basic",
                                                      {"password": "test123"})
        return user_id

    def create_user_test2(self):
        user_id = UserManagementInterface.create_user(self.__admin_user_id,
                                                      "test2",
                                                      "Test",
                                                      "test2@test.com",
                                                      "basic",
                                                      {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        user = UserManagementInterface.read_user_by_id(self.__admin_user_id)

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
        self.assertIsNone(UserManagementInterface.create_user(None,
                                                              "test_other",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        self.assertIsNone(UserManagementInterface.create_user(999,
                                                              "test_other",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with an invalid user name
        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              None,
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with the same user name as another user
        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "test1",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with an invalid display name
        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "test_other",
                                                              None,
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "test_other",
                                                              "",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with an invalid authentication type
        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "test_other",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              None,
                                                              {"password": "test123"}))

        self.assertIsNone(UserManagementInterface.create_user(self.__admin_user_id,
                                                              "test_other",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "",
                                                              {"password": "test123"}))

    def test_read_all_user_ids(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user_ids = UserManagementInterface.read_all_user_ids()

        self.assertEqual(len(user_ids), 3)
        self.assertListEqual(user_ids, [self.__admin_user_id, user_id1, user_id2])

        self.assertNotEqual(self.__admin_user_id, user_id1)
        self.assertNotEqual(self.__admin_user_id, user_id2)
        self.assertNotEqual(user_id1, user_id2)

    def test_read_user_by_user_id(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = UserManagementInterface.read_user_by_id(user_id)

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)
        self.assertIsNotNone(user["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(UserManagementInterface.read_user_by_id(None))
        self.assertIsNone(UserManagementInterface.read_user_by_id(999))

    def test_read_user_by_user_name(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = UserManagementInterface.read_user_by_user_name("test1")

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)
        self.assertIsNotNone(user["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(UserManagementInterface.read_user_by_user_name(None))
        self.assertIsNone(UserManagementInterface.read_user_by_user_name(""))
        self.assertIsNone(UserManagementInterface.read_user_by_user_name("test999"))

    def test_reads_user_by_user_name(self):
        # Create a user and then deactivate it and create a user with the same user name
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                        user_id1,
                                                                        user1["user_name"],
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        False))

        user_id2 = self.create_user_test1()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        # Only active users
        users = UserManagementInterface.read_users_by_user_name("test1", True)
        self.assertEqual(len(users), 1)

        user2 = users[0]

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test1")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test1@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Both active and inactive users
        users = UserManagementInterface.read_users_by_user_name("test1", False)
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
        users = UserManagementInterface.read_users_by_user_name(None, False)
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_user_name("", False)
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_user_name("test999", False)
        self.assertEqual(len(users), 0)

    def test_read_users_by_display_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                        user_id1,
                                                                        user1["user_name"],
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        False))

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        # Only active users
        users = UserManagementInterface.read_users_by_display_name("Test", True)
        self.assertEqual(len(users), 1)

        user2 = users[0]

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Both active and inactive users
        users = UserManagementInterface.read_users_by_display_name("Test", False)
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
        users = UserManagementInterface.read_users_by_display_name(None)
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_display_name("")
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_display_name("Test XYZ")
        self.assertEqual(len(users), 0)

    def test_update_user_invalid_ids(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Try to update a user with a reference to a non-existing "requested by user"
        self.assertFalse(UserManagementInterface.update_user_information(None,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        self.assertFalse(UserManagementInterface.update_user_information(999,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        # Try to update a user with a reference to a non-existing user ID
        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         None,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         999,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

    def test_update_user_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)
        self.assertIsNotNone(user1["revision_id"])

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id1,
                                                                        user_id1,
                                                                        "test1new",
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        user1["active"]))

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1new")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)
        self.assertIsNotNone(user1["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid user name
        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         user_id2,
                                                                         None,
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         user_id2,
                                                                         "",
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        # Try to update a user with the same user name as another user
        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         user_id2,
                                                                         user1["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

    def test_update_display_name(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        "Test New",
                                                                        user2["email"],
                                                                        user2["active"]))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test New")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid display name
        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         None,
                                                                         user2["email"],
                                                                         user2["active"]))

        self.assertFalse(UserManagementInterface.update_user_information(self.__admin_user_id,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         "",
                                                                         user2["email"],
                                                                         user2["active"]))

    def test_update_email(self):
        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        "test2new@test.com",
                                                                        user2["active"]))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

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

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Positive tests ---------------------------------------------------------------------------
        # Disable user
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        False))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], False)
        self.assertIsNotNone(user2["revision_id"])

        # Enable user
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        user2["email"],
                                                                        True))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)
        self.assertIsNotNone(user2["revision_id"])

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         None))

        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         -1))

        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user_id2,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         2))

        # TODO: add test for: find_user_information_history


class UserAuthentication(unittest.TestCase):
    def setUp(self):
        _initialize_system()
        DatabaseInterface.create_new_database()
        self.__admin_user_id = 1

    def create_user_test1(self):
        user_id = UserManagementInterface.create_user(self.__admin_user_id,
                                                      "test1",
                                                      "Test",
                                                      "test1@test.com",
                                                      "basic",
                                                      {"password": "test123"})
        return user_id

    def create_user_test2(self):
        user_id = UserManagementInterface.create_user(self.__admin_user_id,
                                                      "test2",
                                                      "Test",
                                                      "test2@test.com",
                                                      "basic",
                                                      {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        self.assertTrue(UserManagementInterface.authenticate_user("administrator",
                                                                  {"password": "administrator"}))

    def test_users(self):
        self.assertIsNotNone(self.create_user_test1())
        self.assertIsNotNone(self.create_user_test2())

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.authenticate_user("test1",
                                                                  {"password": "test123"}))

        self.assertTrue(UserManagementInterface.authenticate_user("test2",
                                                                  {"password": "test456"}))

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(UserManagementInterface.authenticate_user(None,
                                                                   {"password": "test123"}))

        self.assertFalse(UserManagementInterface.authenticate_user("",
                                                                   {"password": "test456"}))

        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": "Test123"}))

        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": "test456"}))

        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": ""}))

        self.assertFalse(UserManagementInterface.authenticate_user("test2",
                                                                   {"password": "tEst456"}))

        self.assertFalse(UserManagementInterface.authenticate_user("test2",
                                                                   {"password": "test123"}))

    def test_basic_update_update_password(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        self.assertTrue(UserManagementInterface.authenticate_user("test1",
                                                                  {"password": "test123"}))

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_authentication(user_id1,
                                                                           "basic",
                                                                           {"password": "new_pw"}))

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertTrue(UserManagementInterface.authenticate_user("test1",
                                                                  {"password": "new_pw"}))

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": "test123"}))

        # TODO: add test for: others...

if __name__ == '__main__':
    unittest.main()
