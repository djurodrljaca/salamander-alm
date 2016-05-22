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

import connection
import json
import requests
import requests.packages
import signal
import subprocess
import sys
import time
import unittest


class UserManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def setUp(self):
        self.__admin_user_id = 1
        self.__server_instance = subprocess.Popen([sys.executable, "../../server/salamander_alm.py"])

        if self.__server_instance is not None:
            time.sleep(2.0)

    def tearDown(self):
        if self.__server_instance is not None:
            self.__server_instance.send_signal(signal.SIGINT)
            self.__server_instance.wait(1.0)

            if self.__server_instance.returncode is None:
                self.__server_instance.kill()

    # def create_user_test1(self, conn: connection.Connection) -> Optional[dict]:
    #     """
    #     Creates a user
    #     :param conn:
    #     :return:
    #     """
    #     user_id = UserManagementInterface.create_user("test1",
    #                                                   "Test 1",
    #                                                   "test1@test.com",
    #                                                   "basic",
    #                                                   {"password": "test123"})
    #     return user_id

    # Tests ----------------------------------------------------------------------------------------

    def test_default_administrator_login(self):
        conn = connection.Connection()

        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

    def test_default_administrator_login_failure(self):
        conn = connection.Connection()

        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "xyz"})
        self.assertFalse(success)

    def test_default_administrator_logout(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then try to log out
        success = conn.logout()
        self.assertTrue(success)

    def test_default_administrator_logout_failure(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then try to log out
        success = conn.logout()
        self.assertTrue(success)

    def test_default_administrator_read_current_user(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then read the current user
        success = conn.call_get_method("/usermanagement/user")
        self.assertTrue(success)

        user = json.loads(conn.last_response_message.text)
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)

    def test_read_user_by_id(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then read the selected user
        success = conn.call_get_method("/usermanagement/user", parameters={"user_id": 1})
        self.assertTrue(success)

        user = json.loads(conn.last_response_message.text)
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)

    def test_read_user_by_id_failure(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then try to read a non-existing user
        success = conn.call_get_method("/usermanagement/user", parameters={"user_id": 2})
        self.assertFalse(success)

    def test_read_user_by_user_name(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then read the selected user
        success = conn.call_get_method("/usermanagement/user",
                                       parameters={"user_name": "administrator"})
        self.assertTrue(success)

        user = json.loads(conn.last_response_message.text)
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)

    def test_read_user_by_user_name_failure(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then try to read a non-existing user
        success = conn.call_get_method("/usermanagement/user", parameters={"user_name": "xyz"})
        self.assertFalse(success)

    def test_read_user_by_display_name(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then read the selected user
        success = conn.call_get_method("/usermanagement/user",
                                       parameters={"display_name": "Administrator"})
        self.assertTrue(success)

        user = json.loads(conn.last_response_message.text)
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.__admin_user_id)
        self.assertEqual(user["user_name"], "administrator")
        self.assertEqual(user["display_name"], "Administrator")
        self.assertEqual(user["email"], "")
        self.assertEqual(user["active"], True)

    def test_read_user_by_display_name_failure(self):
        conn = connection.Connection()

        # First log in
        success = conn.login("http://127.0.0.1:5000/api",
                             "administrator",
                             {"password": "administrator"})
        self.assertTrue(success)

        # And then try to read a non-existing user
        success = conn.call_get_method("/usermanagement/user",
                                       parameters={"display_name": "xyz"})
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
