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
from database.tables.user import UserSelection
from plugins.database.sqlite.database import DatabaseSqlite
import unittest
from usermanagement.user_management import UserManagementInterface


def _initialize_system():
    # Authentication
    AuthenticationInterface.remove_all_authentication_methods()
    AuthenticationInterface.add_authentication_method(AuthenticationMethodBasic())

    # Database
    DatabaseInterface.load_database_plugin(DatabaseSqlite("database.db"))

    # User management
    # No initialization needed


class UserInformation(unittest.TestCase):
    def setUp(self):
        _initialize_system()
        DatabaseInterface.create_new_database()
        self.__admin_user_id = 1

    @staticmethod
    def create_user_test1():
        user_id = UserManagementInterface.create_user("test1",
                                                      "Test 1",
                                                      "test1@test.com",
                                                      "basic",
                                                      {"password": "test123"})
        return user_id

    @staticmethod
    def create_user_test2():
        user_id = UserManagementInterface.create_user("test2",
                                                      "Test 2",
                                                      "test2@test.com",
                                                      "basic",
                                                      {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        user = UserManagementInterface.read_user_by_id(self.__admin_user_id)

        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)

    def test_read_all_user_ids(self):
        # Create users
        user_id1 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id1)

        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        # Check active users
        user_ids = UserManagementInterface.read_all_user_ids(UserSelection.Active)

        self.assertEqual(len(user_ids), 3)
        self.assertListEqual(user_ids, [self.__admin_user_id, user_id1, user_id2])

        self.assertNotEqual(self.__admin_user_id, user_id1)
        self.assertNotEqual(self.__admin_user_id, user_id2)
        self.assertNotEqual(user_id1, user_id2)

        # Deactivate user
        user1 = UserManagementInterface.read_user_by_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(UserManagementInterface.update_user_information(user_id1,
                                                                        user1["user_name"],
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        False))

        # Recheck active users
        user_ids = UserManagementInterface.read_all_user_ids(UserSelection.Active)

        self.assertEqual(len(user_ids), 2)
        self.assertListEqual(user_ids, [self.__admin_user_id, user_id2])

        # Check inactive users
        user_ids = UserManagementInterface.read_all_user_ids(UserSelection.Inactive)

        self.assertEqual(len(user_ids), 1)
        self.assertListEqual(user_ids, [user_id1])

        # Check all users
        user_ids = UserManagementInterface.read_all_user_ids(UserSelection.All)

        self.assertEqual(len(user_ids), 3)
        self.assertListEqual(user_ids, [self.__admin_user_id, user_id1, user_id2])

    def test_read_user_by_id(self):
        user_id = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = UserManagementInterface.read_user_by_id(user_id)

        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test 1")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(UserManagementInterface.read_user_by_id(999))

    def test_read_user_by_user_name(self):
        user_id = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = UserManagementInterface.read_user_by_user_name("test1")

        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test 1")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(UserManagementInterface.read_user_by_user_name(""))
        self.assertIsNone(UserManagementInterface.read_user_by_user_name("test999"))

    def test_reads_user_by_user_name(self):
        # Create a user and then deactivate it and create a user with the same user name
        user_id1 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(UserManagementInterface.update_user_information(user_id1,
                                                                        user1["user_name"],
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        False))

        user_id2 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        users = UserManagementInterface.read_users_by_user_name("test1")
        self.assertEqual(len(users), 2)

        user1 = users[0]
        user2 = users[1]

        self.assertEqual(user1["id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test 1")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], False)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test1")
        self.assertEqual(user2["display_name"], "Test 1")
        self.assertEqual(user2["email"], "test1@test.com")
        self.assertEqual(user2["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        users = UserManagementInterface.read_users_by_user_name("")
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_user_name("test999")
        self.assertEqual(len(users), 0)

    def test_read_user_by_display_name(self):
        user_id = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive tests ---------------------------------------------------------------------------
        user = UserManagementInterface.read_user_by_display_name("Test 1")

        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test 1")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        self.assertIsNone(UserManagementInterface.read_user_by_display_name(""))
        self.assertIsNone(UserManagementInterface.read_user_by_display_name("Test XYZ"))

    def test_read_users_by_display_name(self):
        user_id1 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)
        self.assertIsNotNone(user1)

        self.assertTrue(UserManagementInterface.update_user_information(user_id1,
                                                                        user1["user_name"],
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        False))

        user_id2 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id2)

        # Positive tests ---------------------------------------------------------------------------
        users = UserManagementInterface.read_users_by_display_name("Test 1")
        self.assertEqual(len(users), 2)

        user1 = users[0]
        user2 = users[1]

        self.assertEqual(user1["id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test 1")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], False)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test1")
        self.assertEqual(user2["display_name"], "Test 1")
        self.assertEqual(user2["email"], "test1@test.com")
        self.assertEqual(user2["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        users = UserManagementInterface.read_users_by_display_name("")
        self.assertEqual(len(users), 0)

        users = UserManagementInterface.read_users_by_display_name("Test XYZ")
        self.assertEqual(len(users), 0)

    def test_create_user(self):
        # Positive tests ---------------------------------------------------------------------------
        self.assertIsNotNone(UserInformation.create_user_test1())

        # Negative tests ---------------------------------------------------------------------------
        # Try to create a user with an invalid user name
        self.assertIsNone(UserManagementInterface.create_user("",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with the same user name as another user
        self.assertIsNone(UserManagementInterface.create_user("test1",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with an invalid display name: "test123"}))

        self.assertIsNone(UserManagementInterface.create_user("test_other",
                                                              "",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with the same display name as another user
        self.assertIsNone(UserManagementInterface.create_user("test_other",
                                                              "Test 1",
                                                              "test_other@test.com",
                                                              "basic",
                                                              {"password": "test123"}))

        # Try to create a user with an invalid authentication type
        self.assertIsNone(UserManagementInterface.create_user("test_other",
                                                              "Test Other",
                                                              "test_other@test.com",
                                                              "",
                                                              {"password": "test123"}))

    def test_update_user_invalid_user_id(self):
        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        # Try to update a user with a reference to a non-existing user ID
        self.assertFalse(UserManagementInterface.update_user_information(999,
                                                                         user2["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_update_user_name(self):
        user_id1 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertEqual(user1["id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test 1")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)

        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id1,
                                                                        "test1new",
                                                                        user1["display_name"],
                                                                        user1["email"],
                                                                        user1["active"]))

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertEqual(user1["id"], user_id1)
        self.assertEqual(user1["user_name"], "test1new")
        self.assertEqual(user1["display_name"], "Test 1")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid user name
        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         "",
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

        # Try to update a user with the same user name as another user
        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user1["user_name"],
                                                                         user2["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

    def test_update_display_name(self):
        user_id1 = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = UserManagementInterface.read_user_by_id(user_id1)

        self.assertEqual(user1["id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test 1")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertEqual(user1["active"], True)

        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user2["user_name"],
                                                                        "Test New",
                                                                        user2["email"],
                                                                        user2["active"]))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test New")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        # Try to update a user with an invalid display name
        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user2["user_name"],
                                                                         "",
                                                                         user2["email"],
                                                                         user2["active"]))

        # Try to update a user with the same display name as another user
        self.assertFalse(UserManagementInterface.update_user_information(user_id2,
                                                                         user2["user_name"],
                                                                         user1["display_name"],
                                                                         user2["email"],
                                                                         user2["active"]))

    def test_update_email(self):
        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.update_user_information(user_id2,
                                                                        user2["user_name"],
                                                                        user2["display_name"],
                                                                        "test2new@test.com",
                                                                        user2["active"]))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2new@test.com")
        self.assertEqual(user2["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests

    def test_deactivate_activate_user(self):
        user_id2 = UserInformation.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        # Deactivate user
        self.assertTrue(UserManagementInterface.deactivate_user(user_id2))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], False)

        # Activate user
        self.assertTrue(UserManagementInterface.activate_user(user_id2))

        user2 = UserManagementInterface.read_user_by_id(user_id2)

        self.assertEqual(user2["id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test 2")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertEqual(user2["active"], True)

        # Negative tests ---------------------------------------------------------------------------
        # There are no negative tests


class UserAuthentication(unittest.TestCase):
    def setUp(self):
        _initialize_system()
        DatabaseInterface.create_new_database()
        self.__admin_user_id = 1

    @staticmethod
    def create_user_test1():
        user_id = UserManagementInterface.create_user("test1",
                                                      "Test 1",
                                                      "test1@test.com",
                                                      "basic",
                                                      {"password": "test123"})
        return user_id

    @staticmethod
    def create_user_test2():
        user_id = UserManagementInterface.create_user("test2",
                                                      "Test 2",
                                                      "test2@test.com",
                                                      "basic",
                                                      {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        self.assertTrue(UserManagementInterface.authenticate_user("administrator",
                                                                  {"password": "administrator"}))

    def test_read_user_authentication(self):
        user_id = UserInformation.create_user_test1()
        self.assertIsNotNone(user_id)

        user = UserManagementInterface.read_user_by_id(user_id)

        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test 1")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertEqual(user["active"], True)

        # Positive tests ---------------------------------------------------------------------------
        user_authentication = UserManagementInterface.read_user_authentication(user_id)

        self.assertEqual(user_authentication["authentication_type"], "basic")
        self.assertTrue(len(user_authentication["authentication_parameters"]["password_hash"]) > 0)

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(UserManagementInterface.read_user_authentication(999))

    def test_authenticate_user(self):
        self.assertIsNotNone(UserAuthentication.create_user_test1())
        self.assertIsNotNone(UserAuthentication.create_user_test2())

        # Positive tests ---------------------------------------------------------------------------
        self.assertTrue(UserManagementInterface.authenticate_user("test1",
                                                                  {"password": "test123"}))

        self.assertTrue(UserManagementInterface.authenticate_user("test2",
                                                                  {"password": "test456"}))

        # Negative tests ---------------------------------------------------------------------------
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

    def test_update_user_authentication(self):
        user_id1 = UserAuthentication.create_user_test1()
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
        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": "test123"}))

        # Negative tests ---------------------------------------------------------------------------
        self.assertFalse(UserManagementInterface.update_user_authentication(user_id1,
                                                                            "",
                                                                            {"password": "new_pw"}))
        self.assertFalse(UserManagementInterface.update_user_authentication(user_id1,
                                                                            "some_type",
                                                                            {"password": "new_pw"}))

        self.assertTrue(UserManagementInterface.authenticate_user("test1",
                                                                  {"password": "new_pw"}))
        self.assertFalse(UserManagementInterface.authenticate_user("test1",
                                                                   {"password": "test123"}))

if __name__ == '__main__':
    unittest.main()
