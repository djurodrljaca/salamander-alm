import rest_api.application

# Make a (global) reference to the Flask application instance
app = rest_api.application.app

# Load individual parts of the REST API
if app is not None:
    import rest_api.usermanagement
