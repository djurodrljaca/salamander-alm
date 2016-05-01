from database.connection import Connection
from database.database import Database


def main():
    # TODO: remove after testing
    Connection.delete_database()
    Database.create_initial_database()


if __name__ == "__main__":
    main()
