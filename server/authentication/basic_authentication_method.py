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

from authentication.authentication import AuthenticationMethod
import bcrypt
from typing import Optional


class AuthenticationMethodBasic(AuthenticationMethod):
    """
    Base class for an authentication method
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def __del__(self):
        """
        Destructor
        """
        pass

    def authentication_type(self) -> str:
        """
        Returns the supported authentication type

        :return:    Supported authentication type
        """
        return "basic"

    def authenticate(self,
                     input_authentication_parameters: dict,
                     reference_authentication_parameters: dict) -> bool:
        """
        Authenticate

        :param input_authentication_parameters:     Input authentication parameters
        :param reference_authentication_parameters: Reference authentication parameters

        :return:    Success or failure
        """
        if "password" not in input_authentication_parameters.keys():
            return False

        password = input_authentication_parameters["password"]

        if "password_hash" not in reference_authentication_parameters.keys():
            return False

        password_hash = reference_authentication_parameters["password_hash"]

        return bcrypt.checkpw(password, password_hash)

    def generate_reference_authentication_parameters(
            self,
            input_authentication_parameters: dict) -> Optional[dict]:
        """
        Generate reference authentication parameters that can be used for authentication

        :param input_authentication_parameters: Input authentication parameters

        :return:    Reference authentication parameters
        """
        if "password" not in input_authentication_parameters.keys():
            return False

        password = input_authentication_parameters["password"]
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        return {"password_hash": password_hash}
