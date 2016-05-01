import database.connection
import database.database
import database.user_management


def main():
    database.connection.delete_database()
    database.database.create_initial_database()

    admin_user_id = database.user_management.find_user_by_user_name("administrator")

    user_id = database.user_management.create_user_basic_authentication(admin_user_id,
                                                                        "test",
                                                                        "Test",
                                                                        "",
                                                                        "123456")

    print("Created new user: " + str(user_id))

    user_id = database.user_management.create_user_basic_authentication(admin_user_id,
                                                                        "test1",
                                                                        "Test",
                                                                        "",
                                                                        "123456")

    print("Created new user: " + str(user_id))

    user_ids = database.user_management.find_users_by_display_name("Test")

    print("Found users: " + str(user_ids))

    # TODO: authenticate user


if __name__ == "__main__":
    main()
