from authentication.authentication import AuthenticationInterface
from authentication.basic_authentication_method import AuthenticationMethodBasic
from database.database import DatabaseInterface
from plugins.database.sqlite.database import DatabaseSqlite
import rest_api

if __name__ == '__main__':
    # Authentication
    AuthenticationInterface.remove_all_authentication_methods()
    AuthenticationInterface.add_authentication_method(AuthenticationMethodBasic())

    # Database
    DatabaseInterface.load_database_plugin(DatabaseSqlite("database.db"))
    DatabaseInterface.create_new_database()

    # Start server
    rest_api.app.run(debug=True)
