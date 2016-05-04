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

import bcrypt


def generate_password_hash(password: str) -> str:
    """
    Generates a hash of the specified password

    :param password: Password

    :return: Password hash
    """
    return bcrypt.hashpw(password, bcrypt.gensalt())


def authenticate(password: str, password_hash: str) -> bool:
    """
    Tries to authenticate the specified password with the specified password hash

    :param password: Password
    :param password_hash: Password hash

    :return: Authentication result
    """
    return bcrypt.checkpw(password, password_hash)
