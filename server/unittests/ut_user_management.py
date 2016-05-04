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
                                                             {"password": "test123"})
        return user_id

    def test_default_administrator(self):
        user = usermanagement.user_management.find_user_by_user_id(self.admin_user_id)

        self.assertEqual(user["user_id"], self.admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertIsNotNone(user["revision_id"])

    def test_create_user(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

    def test_find_user_by_user_id(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        user = usermanagement.user_management.find_user_by_user_id(user_id)

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertIsNotNone(user["revision_id"])

    def test_find_user_by_user_name(self):
        user_id = self.create_user_test1()
        self.assertIsNotNone(user_id)

        user = usermanagement.user_management.find_user_by_user_name("test1")

        self.assertEqual(user["user_id"], user_id)
        self.assertEqual(user["user_name"], "test1")
        self.assertEqual(user["display_name"], "Test")
        self.assertEqual(user["email"], "test1@test.com")
        self.assertIsNotNone(user["revision_id"])

    def test_find_users_by_display_name(self):
        user_id1 = self.create_user_test1()
        self.assertIsNotNone(user_id1)

        user_id2 = self.create_user_test2()
        self.assertIsNotNone(user_id2)

        users = usermanagement.user_management.find_users_by_display_name("Test")
        self.assertEqual(len(users), 2)

        user1 = None
        user2 = None

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

    # TODO: add negative tests
    # TODO: add test for: find_users_by_email
    # TODO: add test for: find_user_information_history

# TODO: add test cases for: user_authentication


if __name__ == '__main__':
    unittest.main()
