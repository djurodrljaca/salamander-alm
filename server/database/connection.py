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

import os
import os.path
import sqlite3


# File path to the database
_file_path = "database.db"


def delete_database() -> None:
    """
    Deletes the database
    """
    if os.path.exists(_file_path):
        os.remove(_file_path)


def create() -> sqlite3.Connection:
    """
    Creates a connection to the database

    :return: Database connection
    """
    connection = sqlite3.connect(_file_path)
    connection.row_factory = sqlite3.Row

    return connection
