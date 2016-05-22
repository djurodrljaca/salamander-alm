from database.database import DatabaseInterface
from flask import jsonify
from flask_restful import request, abort
from rest_api.restricted_resource import RestrictedResource
from usermanagement.user_management import UserManagementInterface


class User(RestrictedResource):
    """
    REST API for logging out
    """

    def __init__(self):
        """
        Constructor
        """
        RestrictedResource.__init__(self)

    def get(self):
        """
        Read user information

        :return:    User information object

        Allowed parameters (max one can be used):

        - user_id:      int
        - user_name:    str
        - display_name: str

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        # Extract session token from the request
        token = RestrictedResource._read_session_token()

        # Extract arguments
        args = request.args

        if args is None:
            abort(400, message="Parameter is missing")

        # Read current user
        if (("user_id" not in args) and
                ("user_name" not in args) and
                ("display_name" not in args)):
            return User.__read_current_user(token)

        # Read user by user ID
        elif (("user_id" in args) and
                  ("user_name" not in args) and
                  ("display_name" not in args) and
                  ("user_selection" not in args)):
            return User.__read_user_by_user_id(token, args["user_id"])

        # Read user by user name
        elif (("user_name" in args) and
                  ("user_id" not in args) and
                  ("display_name" not in args)):
            return User.__read_user_by_user_name(token, args["user_name"])

        # Read user by display name
        elif (("display_name" in args) and
                  ("user_id" not in args) and
                  ("user_name" not in args)):
            return User.__read_user_by_display_name(token, args["display_name"])

        else:
            abort(400, message="Invalid parameters")

    @staticmethod
    def __read_current_user(token: str) -> dict:
        """
        Reads current user's information

        :param token:   Session token which contains the current user's information

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        session_user = None
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Extract session user
            if success:
                session_user = RestrictedResource._read_session_user(connection, token)

                if session_user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return user
        if success:
            return jsonify(session_user)
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")

    @staticmethod
    def __read_user_by_user_id(token: str, user_id: int) -> dict:
        """
        Reads current user's information

        :param token:   Session token which contains the current user's information
        :param user_id: ID of the user to read

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        user = None
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Extract session user
            if success:
                session_user = RestrictedResource._read_session_user(connection, token)

                if session_user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            # Read requested user
            if success:
                user = UserManagementInterface.read_user_by_id(connection, user_id)

                if user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid user ID"

            connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return user
        if success:
            return jsonify(user)
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")

    @staticmethod
    def __read_user_by_user_name(token: str, user_name: str) -> dict:
        """
        Reads current user's information

        :param token:       Session token which contains the current user's information
        :param user_name:   User name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        user = None
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Extract session user
            if success:
                session_user = RestrictedResource._read_session_user(connection, token)

                if session_user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            # Read requested user
            if success:
                user = UserManagementInterface.read_user_by_user_name(connection, user_name)

                if user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid user name"

            connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return user
        if success:
            return jsonify(user)
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")

    @staticmethod
    def __read_user_by_display_name(token: str, display_name: str) -> dict:
        """
        Reads current user's information

        :param token:           Session token which contains the current user's information
        :param display_name:    Display name

        :return:    User information object

        Returned dictionary contains items:

        - id
        - user_name
        - display_name
        - email
        - active
        """
        user = None
        success = False
        error_code = None
        error_message = None

        connection = DatabaseInterface.create_connection()

        try:
            success = connection.begin_transaction()

            # Extract session user
            if success:
                session_user = RestrictedResource._read_session_user(connection, token)

                if session_user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid session token"

            # Read requested user
            if success:
                user = UserManagementInterface.read_user_by_display_name(connection, display_name)

                if user is None:
                    success = False
                    error_code = 400
                    error_message = "Invalid user name"

            connection.rollback_transaction()
        except:
            connection.rollback_transaction()
            abort(500, message="Internal error, please try again")

        # Return user
        if success:
            return jsonify(user)
        else:
            if (error_code is not None) and (error_message is not None):
                abort(error_code, message=error_message)
            else:
                abort(500, message="Internal error")
