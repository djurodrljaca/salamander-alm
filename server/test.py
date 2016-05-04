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

import database.connection
import database.database
import usermanagement
import usermanagement.user_management


def main():
    database.connection.delete_database()
    database.database.create_initial_database()

    admin_user = usermanagement.user_management.find_user_by_user_name("administrator")

    user_id = usermanagement.user_management.create_user(admin_user["user_id"],
                                                         "test",
                                                         "Test",
                                                         "test@example.com",
                                                         "basic",
                                                         {"password": "123456"})
    print("Created new user: " + str(user_id))

    user_id = usermanagement.user_management.create_user(admin_user["user_id"],
                                                         "test1",
                                                         "Test",
                                                         "test1@example.com",
                                                         "basic",
                                                         {"password": "123456"})
    print("Created new user: " + str(user_id))

    user = usermanagement.user_management.find_user_by_user_name("administrator")
    print("Found user: " + str(user))

    user = usermanagement.user_management.find_user_by_user_name("test")
    print("Found user: " + str(user))

    user = usermanagement.user_management.find_user_by_user_name("test1")
    print("Found user: " + str(user))

    print("Modifying user information...")
    usermanagement.user_management.modify_user_information(admin_user["user_id"],
                                                           user["user_id"],
                                                           user["user_name"],
                                                           user["display_name"],
                                                           "john.smith@example.com",
                                                           True)
    user = usermanagement.user_management.find_user_by_user_id(user["user_id"])
    print("Found user: " + str(user))

    users = usermanagement.user_management.find_users_by_display_name("Test")
    print("Found users: " + str(users))

    print("Modifying user information...")
    usermanagement.user_management.modify_user_information(admin_user["user_id"],
                                                           user["user_id"],
                                                           user["user_name"],
                                                           user["display_name"],
                                                           user["email"],
                                                           False)
    user = usermanagement.user_management.find_user_by_user_id(user["user_id"])
    print("Found user: " + str(user))

    users = usermanagement.user_management.find_users_by_display_name("Test")
    print("Found users: " + str(users))

    authenticated = usermanagement.user_management.authenticate_user("administrator",
                                                                     {"password": "administrator"})
    print("User authenticated: " + str(authenticated))

    authenticated = usermanagement.user_management.authenticate_user("test",
                                                                     {"password": "123456"})
    print("User authenticated: " + str(authenticated))

    authenticated = usermanagement.user_management.authenticate_user("test",
                                                                     {"password": "654321"})
    print("User authenticated: " + str(authenticated))

    print("Modifying user authentication...")
    user = usermanagement.user_management.find_user_by_user_name("test")
    usermanagement.user_management.modify_user_authentication(admin_user["user_id"],
                                                              user["user_id"],
                                                              "basic",
                                                              {"password": "654321"})
    authenticated = usermanagement.user_management.authenticate_user("test",
                                                                     {"password": "123456"})
    print("User authenticated: " + str(authenticated))

    authenticated = usermanagement.user_management.authenticate_user("test",
                                                                     {"password": "654321"})
    print("User authenticated: " + str(authenticated))


if __name__ == "__main__":
    main()
