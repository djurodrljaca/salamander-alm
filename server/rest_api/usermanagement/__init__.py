from rest_api.application import api
from rest_api.usermanagement import login, logout


def _create_url(relative_url: str) -> str:
    """
    Creates a full URL from a relative URL

    :param relative_url:    Relative part of the URL

    :return:    Full URL

    Example:
    - Relative URL: "login"
    - Returned URL: "/api/usermanagement/login"
    """
    return "/api/usermanagement/" + relative_url


if api is not None:
    # Add all resources from this package
    api.add_resource(login.Login, _create_url("login"))
    api.add_resource(logout.Logout, _create_url("logout"))
