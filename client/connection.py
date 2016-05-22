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

import enum
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib.parse
from typing import Optional


class CertificateVerification(enum.Enum):
    """
    Certificate verification
    """
    Disabled = 0
    Enabled = 1


class Connection(object):
    """
    Connection to the server.

    During login the REST API URL, authentication parameters and certificate verification options
    are supplied. After a successful login HTTP methods (DELETE, GET, POST, PUT) can be called
    and this class will prepare all the data needed to successfully call the method.

    The data that will be prepared is:
    * the full URL for the method (base URL combined with relative URL and additional parameters)
    * authentication parameters (authentication ID and token)
    * other options (certificate verification)

    Below are some examples of URL's mentioned above.

    Example without parameters:
    * base URL:     "https://salamander_alm.example.com:443/api"
    * relative URL: "/usermanagement/login"
    * full URL:     "https://salamander_alm.example.com:443/api/usermanagement/login"

    Example with single parameter:
    * base URL:     "https://salamander_alm.example.com:443/api"
    * relative URL: "/projectmanagement/projects"
    * parameters:   {"limit": 10}
    * full URL:     "https://salamander_alm.example.com:443/api/projectmanagement/projects?limit=10"

    Example with multiple parameters:
    * base URL:     "https://salamander_alm.example.com:443/api"
    * relative URL: "/projectmanagement/projects"
    * parameters:   {"limit": 10, "offset": 50}
    * full URL:     "https://salamander_alm.example.com:443/api/projectmanagement/projects?
                     limit=10&offset=50"
    """

    def __init__(self):
        """
        Constructor
        """
        self._isLoggedIn = False
        self._baseUrl = ""
        self._loginToken = _LoginToken()
        self._verifyCertificate = True
        self._authenticationHeaders = None
        self._lastResponseMessage = None

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._clear()

    def is_logged_in(self):
        """
        Check if logged in

        :return: Success or failure
        :rtype: bool
        """
        return self._isLoggedIn

    def login(self,
              base_url: str,
              user_name: str,
              authentication_parameters: dict,
              certificate_verification=CertificateVerification.Enabled) -> bool:
        """
        Log in to the server

        :param base_url:                    URL of the selected Tuleap instance
                                            (example: https://salamander_alm.example.com:443/api)
        :param user_name:                   User name
        :param authentication_parameters:   Authentication parameters
        :param certificate_verification:    Enable or disable certificate verification

        :return:    Success or failure
        """
        # Clear last response message
        self._lastResponseMessage = None

        # Log out if already logged in
        if self.is_logged_in():
            self.logout()

        # Get login token
        url = base_url + "/usermanagement/login"
        data = {"user_name": user_name, "authentication_parameters": authentication_parameters}
        verify_certificate = (certificate_verification == CertificateVerification.Enabled)

        response = requests.post(url, json=data, verify=verify_certificate)
        self._lastResponseMessage = response

        # parse response
        success = self._loginToken.parse(response)

        if success:
            # Save connection to the server
            self._baseUrl = base_url
            self._isLoggedIn = True
            self._verifyCertificate = verify_certificate
            self._authenticationHeaders = {"SALM-Session-Token": self._loginToken.token}
            success = True

        return success

    def logout(self) -> bool:
        """
        Log out of the server

        :return: success: Success or failure
        """
        # Clear last response message
        self._lastResponseMessage = None

        # Check if logged in
        if not self.is_logged_in():
            # Not logged in
            return True

        # Logout
        relative_url = "/usermanagement/logout"

        success = self.call_post_method(relative_url)

        # Clean up after logout
        self._clear()

        return success

    def call_delete_method(self,
                           relative_url: str,
                           parameters=None,
                           success_status_codes=list([200])):
        """
        Call DELETE method on the server

        :param relative_url:            Relative part of URL
        :param parameters:              Parameters that should be added to the URL (dictionary)
        :param success_status_codes:    List of HTTP status codes that represent 'success'

        :return:    Success or failure

        Note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None

        # Check if logged in
        if not self.is_logged_in():
            return False

        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False

        # Call the DELETE method
        url = self._create_full_url(relative_url, parameters)

        self._lastResponseMessage = requests.delete(url,
                                                    headers=self._authenticationHeaders,
                                                    verify=self._verifyCertificate)

        # Check for success
        if self._lastResponseMessage.status_code in success_status_codes:
            return True
        else:
            return False

    def call_get_method(self, relative_url: str, parameters=None, success_status_codes=list([200])):
        """
        Call GET method on the server

        :param relative_url:            Relative part of URL
        :param parameters:              Parameters that should be added to the URL (dictionary)
        :param success_status_codes:    List of HTTP status codes that represent 'success'

        :return:    Success or failure

        Note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None

        # Check if logged in
        if not self.is_logged_in():
            return False

        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False

        # Call the GET method
        url = self._create_full_url(relative_url, parameters)

        self._lastResponseMessage = requests.get(url,
                                                 headers=self._authenticationHeaders,
                                                 verify=self._verifyCertificate)

        # Check for success
        if self._lastResponseMessage.status_code in success_status_codes:
            return True
        else:
            return False

    def call_post_method(self, relative_url: str, data=None, success_status_codes=list([200])):
        """
        Call POST method on the server

        :param relative_url:            Relative part of URL
        :param data:                    Request data (will be converted to json)
        :param success_status_codes:    List of HTTP status codes that represent 'success'

        :return:    Success or failure

        Note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None

        # Check if logged in
        if not self.is_logged_in():
            return False

        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False

        # Call the POST method
        url = self._create_full_url(relative_url)

        self._lastResponseMessage = requests.post(url,
                                                  json=data,
                                                  headers=self._authenticationHeaders,
                                                  verify=self._verifyCertificate)

        # Check for success
        if self._lastResponseMessage.status_code in success_status_codes:
            return True
        else:
            return False

    # TODO: create PUT method?

    def get_last_response_message(self) -> Optional[requests.Response]:
        """
        Get last response message

        :return:    Last response message

        Note: This could be useful for diagnostic purposes when an error occurs
        """
        return self._lastResponseMessage

    def _create_full_url(self, relative_url: str, parameters=None) -> str:
        """
        Create "full" URL from a "relative" URL. "Full" URL is created by combining REST API URL
        with "relative" URL and optional parameters.

        :param relative_url:    Relative part of URL
        :param parameters:      Parameters that should be appended to the URL (dictionary)

        :return:    Full URL
        """
        url = self._baseUrl + relative_url

        if parameters is not None:
            if len(parameters) > 0:
                url = url + "?" + urllib.parse.urlencode(parameters)

        return url

    def _clear(self):
        """
        Clear all members
        """
        self._isLoggedIn = False
        self._baseUrl = ""
        self._loginToken = _LoginToken()
        self._verifyCertificate = True
        self._authenticationHeaders = None
        self._lastResponseMessage = None


class _LoginToken(object):
    """
    Login token
    """

    def __init__(self):
        """
        Constructor
        """
        self.token = ""

    def parse(self, response: requests.Response) -> bool:
        """
        Parse response object for login data

        :param response:    Response message from server

        :return:    Success or failure
        """
        if response.status_code != 200:
            return False

        response_data = json.loads(response.text)

        # Save login token
        token = response_data["session_token"]

        self.token = token
        return True
