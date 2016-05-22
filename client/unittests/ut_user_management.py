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

import json
import requests
import requests.packages
import signal
import subprocess
import sys
import time
import unittest


class Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def setUp(self):
        self.server_instance = subprocess.Popen([sys.executable, "../../server/salamander_alm.py"])

        if self.server_instance is not None:
            time.sleep(3.0)

    def tearDown(self):
        if self.server_instance is not None:
            self.server_instance.send_signal(signal.SIGINT)
            self.server_instance.wait(3.0)

            if self.server_instance.returncode is None:
                self.server_instance.kill()

    def test_login(self):
        response = requests.post("http://127.0.0.1:5000/api/usermanagement/login",
                                 json={"user_name": "administrator",
                                       "authentication_parameters": {"password": "administrator"}})
        self.assertEqual(response.status_code, 200, "Response: " + response.text)

        response_data = json.loads(response.text)
        self.assertIsNotNone(response_data["session_token"])

        print("Session token:" + response_data["session_token"])

    def test_login_failure(self):
        response = requests.post("http://127.0.0.1:5000/api/usermanagement/login",
                                 json={"user_name": "administrator",
                                       "authentication_parameters": {"password": "xyz"}})
        self.assertEqual(response.status_code, 400, "Response: " + response.text)


if __name__ == '__main__':
    unittest.main()
