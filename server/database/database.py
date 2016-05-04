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

import authentication.basic
import datetime
import database.connection
import database.tables.revision
import database.tables.user
import database.tables.user_authentication
import database.tables.user_authentication_basic
import database.tables.user_information
import sqlite3


def create_initial_database() -> None:
    """
    Creates initial database
    """
    with database.connection.create() as connection:
        # Create tables and indexes
        database.tables.revision.create_table(connection)
        database.tables.revision.create_indexes(connection)

        database.tables.user.create_table(connection)
        database.tables.user.create_indexes(connection)

        database.tables.user_authentication.create_table(connection)
        database.tables.user_authentication.create_indexes(connection)

        database.tables.user_authentication_basic.create_table(connection)
        database.tables.user_authentication_basic.create_indexes(connection)

        database.tables.user_information.create_table(connection)
        database.tables.user_information.create_indexes(connection)

        # Create initial system users and user groups
        _create_initial_system_users(connection)
        _create_initial_system_user_groups(connection)


def _create_initial_system_users(connection: sqlite3.Connection) -> None:
    """
    Creates the initial system users:
    - "Administrator"
    """
    # Since the database doesn't contain any users we must first create just the ID of the
    # Administrator user, then create the first revision that is referencing the Administrator
    # and then finally write all of the other user information
    user_id = database.tables.user.insert_record(connection)
    revision_id = database.tables.revision.insert_record(connection,
                                                         datetime.datetime.utcnow(),
                                                         user_id)
    database.tables.user_information.insert_record(connection,
                                                   user_id,
                                                   "administrator",
                                                   "Administrator",
                                                   "",
                                                   True,
                                                   revision_id)

    user_authentication_id = database.tables.user_authentication.insert_record(
        connection,
        user_id,
        "basic",
        revision_id)

    database.tables.user_authentication_basic.insert_record(
        connection,
        user_authentication_id,
        authentication.basic.generate_password_hash("administrator"),
        revision_id)


def _create_initial_system_user_groups(connection: sqlite3.Connection) -> None:
    """
    Creates the initial system users:
    - "Administrators"
    """
    # TODO: implement
    return

