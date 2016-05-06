import database.connection
import database.database
import usermanagement.user_management
import unittest


def _initialize_database():
    database.connection.delete_database()
    database.database.create_initial_database()


class UserInformation(unittest.TestCase):
    def setUp(self):
        _initialize_database()
        self.admin_user_id = 1

    def create_user_test1(self):
        user_id = usermanagement.user_management.create_user(self.admin_user_id,
                                                             "test1",
                                                             "Test",
                                                             "test1@test.com",
                                                             "basic",
                                                             {"password": "test123"})
        return user_id
    
    def create_user_test2(self):
        user_id = usermanagement.user_management.create_user(self.admin_user_id,
                                                             "test2",
                                                             "Test",
                                                             "test2@test.com",
                                                             "basic",
                                                             {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        user = usermanagement.user_management.find_user_by_user_id(self.admin_user_id)

        self.assertEqual(user["user_id"], self.admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertIsNotNone(user["revision_id"])

    def test_create_user(self):
        # Positive test
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Negative test
        # Try to create a user with the same user name
        user_id = usermanagement.user_management.create_user(self.admin_user_id,
                                                             "test1",
                                                             "Test Other",
                                                             "test_other@test.com",
                                                             "basic",
                                                             {"password": "test123"})
        self.assertIsNone(user_id)

    def test_find_user_by_user_id(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive test
        user = usermanagement.user_management.find_user_by_user_id(user_id)

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertIsNotNone(user["revision_id"])

        # Negative test
        user = usermanagement.user_management.find_user_by_user_id(999)
        self.assertIsNone(user)

    def test_find_user_by_user_name(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        # Positive test
        user = usermanagement.user_management.find_user_by_user_name("test1")

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertIsNotNone(user["revision_id"])

        # Negative test
        user = usermanagement.user_management.find_user_by_user_name("test999")
        self.assertIsNone(user)

    def test_find_users_by_display_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        # Positive test
        users = usermanagement.user_management.find_users_by_display_name("Test")
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
        self.assertIsNotNone(user1["revision_id"])

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertIsNotNone(user2["revision_id"])

        # Negative test
        users = usermanagement.user_management.find_users_by_display_name("Test XYZ")
        self.assertEqual(len(users), 0)

    def test_modify_user_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user1 = usermanagement.user_management.find_user_by_user_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertIsNotNone(user1["revision_id"])

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        user2 = usermanagement.user_management.find_user_by_user_id(user_id2)

        self.assertEqual(user2["user_id"], user_id2)
        self.assertEqual(user2["user_name"], "test2")
        self.assertEqual(user2["display_name"], "Test")
        self.assertEqual(user2["email"], "test2@test.com")
        self.assertIsNotNone(user2["revision_id"])

        # Positive test
        self.assertTrue(
            usermanagement.user_management.modify_user_information(user_id1,
                                                                   user_id1,
                                                                   "test1new",
                                                                   user1["display_name"],
                                                                   user1["email"],
                                                                   True))

        user1 = usermanagement.user_management.find_user_by_user_id(user_id1)

        self.assertEqual(user1["user_id"], user_id1)
        self.assertEqual(user1["user_name"], "test1new")
        self.assertEqual(user1["display_name"], "Test")
        self.assertEqual(user1["email"], "test1@test.com")
        self.assertIsNotNone(user1["revision_id"])

        # Negative test
        self.assertTrue(
            usermanagement.user_management.modify_user_information(user_id2,
                                                                   user_id2,
                                                                   "test1new",
                                                                   user2["display_name"],
                                                                   user2["email"],
                                                                   True))

    # TODO: add test for: modify_display_name
    # TODO: add test for: modify_email
    # TODO: add test for: disable_user
    # TODO: add test for: enable_user
    # TODO: add test for: find_user_information_history


class UserAuthentication(unittest.TestCase):
    def setUp(self):
        _initialize_database()
        self.admin_user_id = 1

    def create_user_test1(self):
        user_id = usermanagement.user_management.create_user(self.admin_user_id,
                                                             "test1",
                                                             "Test",
                                                             "test1@test.com",
                                                             "basic",
                                                             {"password": "test123"})
        return user_id

    def create_user_test2(self):
        user_id = usermanagement.user_management.create_user(self.admin_user_id,
                                                             "test2",
                                                             "Test",
                                                             "test2@test.com",
                                                             "basic",
                                                             {"password": "test456"})
        return user_id

    def test_default_administrator(self):
        self.assertTrue(
            usermanagement.user_management.authenticate_user("administrator",
                                                             {"password": "administrator"}))

    def test_users(self):
        self.create_user_test1()
        self.create_user_test2()

        # Positive test
        self.assertTrue(
            usermanagement.user_management.authenticate_user("test1",
                                                             {"password": "test123"}))
        self.assertTrue(
            usermanagement.user_management.authenticate_user("test2",
                                                             {"password": "test456"}))

        # Negative test
        self.assertFalse(
            usermanagement.user_management.authenticate_user("test1",
                                                             {"password": "Test123"}))
        self.assertFalse(
            usermanagement.user_management.authenticate_user("test2",
                                                             {"password": "tEst456"}))

    # TODO: add test for: find_user_information_history
    # TODO: add test for: others...

if __name__ == '__main__':
    unittest.main()
