import database.connection
import database.database
import database.user_management


def main():
    database.connection.delete_database()
    database.database.create_initial_database()

    admin_user = database.user_management.find_user_by_user_name("administrator")

    user_id = database.user_management.create_user_basic_authentication(admin_user["id"],
                                                                        "test",
                                                                        "Test",
                                                                        "",
                                                                        "123456")

    print("Created new user: " + str(user_id))

    user_id = database.user_management.create_user_basic_authentication(admin_user["id"],
                                                                        "test1",
                                                                        "Test",
                                                                        "",
                                                                        "123456")

    print("Created new user: " + str(user_id))

    user = database.user_management.find_user_by_user_name("administrator")

    print("Found users: " + str(user))

    user = database.user_management.find_user_by_user_name("test")

    print("Found users: " + str(user))

    user = database.user_management.find_user_by_user_name("test1")

    print("Found users: " + str(user))

    users = database.user_management.find_users_by_display_name("Test")

    print("Found users: " + str(users))

    authenticated = database.user_management.authenticate_user_basic_authentication("administrator",
                                                                                    "administrator")

    print("User authenticated: " + str(authenticated))

    authenticated = database.user_management.authenticate_user_basic_authentication("test",
                                                                                    "123456")

    print("User authenticated: " + str(authenticated))

    authenticated = database.user_management.authenticate_user_basic_authentication("test",
                                                                                    "xxxxxx")

    print("User authenticated: " + str(authenticated))


if __name__ == "__main__":
    main()
