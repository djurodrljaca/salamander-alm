import database.connection
import database.database
import database.user_management


def main():
    database.connection.delete_database()
    database.database.create_initial_database()

    admin_user = database.user_management.find_user_by_user_name("administrator")

    user_id = database.user_management.create_user(admin_user["user_id"],
                                                   "test",
                                                   "Test",
                                                   "test@example.com",
                                                   "basic",
                                                   {"password": "123456"})
    print("Created new user: " + str(user_id))

    user_id = database.user_management.create_user(admin_user["user_id"],
                                                   "test1",
                                                   "Test",
                                                   "test1@example.com",
                                                   "basic",
                                                   {"password": "123456"})
    print("Created new user: " + str(user_id))

    user = database.user_management.find_user_by_user_name("administrator")
    print("Found user: " + str(user))

    user = database.user_management.find_user_by_user_name("test")
    print("Found user: " + str(user))

    user = database.user_management.find_user_by_user_name("test1")
    print("Found user: " + str(user))

    database.user_management.modify_user_information(admin_user["user_id"],
                                                     user["user_id"],
                                                     user["user_name"],
                                                     user["display_name"],
                                                     "john.smith@example.com",
                                                     True)
    user = database.user_management.find_user_by_user_id(user["user_id"])
    print("Found user: " + str(user))

    users = database.user_management.find_users_by_display_name("Test")
    print("Found users: " + str(users))

    database.user_management.modify_user_information(admin_user["user_id"],
                                                     user["user_id"],
                                                     user["user_name"],
                                                     user["display_name"],
                                                     user["email"],
                                                     False)
    user = database.user_management.find_user_by_user_id(user["user_id"])
    print("Found user: " + str(user))

    users = database.user_management.find_users_by_display_name("Test")
    print("Found users: " + str(users))

    authenticated = database.user_management.authenticate_user("administrator",
                                                               {"password": "administrator"})
    print("User authenticated: " + str(authenticated))

    authenticated = database.user_management.authenticate_user("test",
                                                               {"password": "123456"})
    print("User authenticated: " + str(authenticated))

    authenticated = database.user_management.authenticate_user("test",
                                                               {"password": "xxxxxx"})
    print("User authenticated: " + str(authenticated))


if __name__ == "__main__":
    main()
