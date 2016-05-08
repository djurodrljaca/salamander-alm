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

from typing import Optional


class AuthenticationMethod(object):
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
        raise NotImplementedError()

    def authenticate(self,
                     input_authentication_parameters: dict,
                     reference_authentication_parameters: dict) -> bool:
        """
        Authenticate

        :param input_authentication_parameters:     Input authentication parameters
        :param reference_authentication_parameters: Reference authentication parameters

        :return:    Success or failure
        """
        raise NotImplementedError()

    def generate_reference_authentication_parameters(
            self,
            input_authentication_parameters: dict) -> Optional[dict]:
        """
        Generate reference authentication parameters that can be used for authentication

        :param input_authentication_parameters: Input authentication parameters

        :return:    Reference authentication parameters
        """
        raise NotImplementedError()


class Authentication(object):
    """
    Class for user authentication
    """

    def __init__(self):
        """
        Constructor
        """
        self.__authentication_methods = list()

    def authenticate(self,
                     authentication_type: str,
                     input_authentication_parameters: dict,
                     reference_authentication_parameters: dict) -> bool:
        """
        Authenticate

        :param authentication_type:                 Authentication type
        :param input_authentication_parameters:     Input authentication parameters
        :param reference_authentication_parameters: Reference authentication parameters

        :return:    Success or failure
        """
        success = False
        authentication_method = self.__find_authentication_method(authentication_type)

        if authentication_method is not None:
            success = authentication_method.authenticate(input_authentication_parameters,
                                                         reference_authentication_parameters)

        return success

    def generate_reference_authentication_parameters(
            self,
            authentication_type: str,
            input_authentication_parameters: dict,) -> Optional[dict]:
        """
        Generate reference authentication parameters that can be used for authentication

        :param authentication_type:             Authentication type
        :param input_authentication_parameters: Input authentication parameters

        :return:    Reference authentication parameters
        """
        reference_authentication_parameters = None
        authentication_method = self.__find_authentication_method(authentication_type)

        if authentication_method is not None:
            reference_authentication_parameters = \
                authentication_method.generate_reference_authentication_parameters(
                    input_authentication_parameters)

        return reference_authentication_parameters

    def add_authentication_method(self, authentication_method: AuthenticationMethod) -> bool:
        """
        Adds support for an authentication method

        :param authentication_method:   Authentication method

        :return:    Success or failure
        """
        success = False
        existing_authentication_method = self.__find_authentication_method(
            authentication_method.authentication_type())

        if existing_authentication_method is None:
            self.__authentication_methods.append(authentication_method)
            success = True

        return success

    def remove_all_authentication_methods(self) -> None:
        """
        Removes all authentication methods
        """
        self.__authentication_methods.clear()

    def __find_authentication_method(self,
                                     authentication_type: str) -> Optional[AuthenticationMethod]:
        """
        Find authentication method

        :param authentication_type: Authentication type

        :return:    Authentication method
        """
        for item in self.__authentication_methods:
            if item.authentication_type() == authentication_type:
                return item

        return None
