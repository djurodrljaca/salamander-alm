from database.database import DatabaseInterface
from flask_restful import abort
from rest_api.restricted_resource import RestrictedResource
from usermanagement.user_management import UserManagementInterface


class Logout(RestrictedResource):
    """
    REST API for logging out
    """

    def __init__(self):
        """
        Constructor
        """
        RestrictedResource.__init__(self)

    def post(self):
        """
        Logs out the user
        """
        # Extract session token from the request
        token = self._read_session_token()

        # Log out
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Get the session token
            session_token = None

            if success:
                session_token = UserManagementInterface.read_session_token(connection, token)

                if session_token is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            # Delete session token
            if success:
                success = UserManagementInterface.delete_session_token(connection, token)

                if not success:
                    error_code = 500
                    error_message = "Failed to log out, please try again"

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return response
        if success:
            return None
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")
