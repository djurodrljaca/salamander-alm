from database.database import DatabaseInterface
from flask import jsonify
from flask_restful import Resource, request, abort
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

    def post(self):
        """
        Logs in a user with the specified parameters

        :return:    Session token
        """
        # Extract arguments from the request
        request_data = request.get_json()

        if ("user_name" not in request_data) or ("authentication_parameters" not in request_data):
            abort(400, message="Missing parameters")

        # Log in
        token = None
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
                    request_data["user_name"],
                    request_data["authentication_parameters"])

                if user_id is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid user name or authentication parameters"

            # Create session token
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
