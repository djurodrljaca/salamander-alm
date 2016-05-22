from database.database import DatabaseInterface
from flask import jsonify
from flask_restful import Resource, reqparse, abort
from usermanagement.user_management import UserManagementInterface


class Login(Resource):
    """
    REST API for logging in
    """

    def __init__(self):
        """
        Constructor
        """
        Resource.__init__(self)

        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('user_name', type=str, required=True)
        self.request_parser.add_argument('authentication_parameters', type=dict, required=True)

    def post(self):
        """
        Tries to log in the user with the specified parameters

        :return:    Tuple with user session token
        """
        # Extract arguments from the request
        args = self.request_parser.parse_args(strict=True)

        # Login
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Authenticate the user
            user_id = None

            if success:
                user_id = UserManagementInterface.authenticate_user(
                    connection,
                    args["user_name"],
                    args["authentication_parameters"])

                if user_id is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid user name or authentication parameters"

            # Create session token
            token = None

            if success:
                token = UserManagementInterface.create_session_token(connection, user_id)

                if token is None:
                    success = False
                    error_code = 500
                    error_message = "Failed to generate a session token, please try again"

            if success:
                connection.commit_transaction()
            else:
                connection.rollback_transaction()
        except Exception as e:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return response
        if success:
            return jsonify({'session_token': token})
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")
