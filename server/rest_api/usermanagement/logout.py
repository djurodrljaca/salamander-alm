from database.database import DatabaseInterface
from flask import jsonify
from flask_restful import Resource, reqparse, abort
from usermanagement.user_management import UserManagementInterface


class Logout(Resource):
    """
    REST API for logging out
    """

    def __init__(self):
        """
        Constructor
        """
        Resource.__init__(self)

        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('SALM-Session-Token',
                                         type=str,
                                         required=True,
                                         location="headers",
                                         dest="token")

    def post(self):
        """
        Tries to log out the user

        :return:    Tuple with user session token
        """
        # Extract arguments from the request
        args = self.request_parser.parse_args(strict=True)

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
                session_token = UserManagementInterface.read_session_token(connection,
                                                                           args["token"])

                if session_token is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            if success:
                success = UserManagementInterface.delete_session_token(connection, args["token"])

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
                print("Error code: " + str(error_code))
                print("Error message: " + error_message)

                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")
