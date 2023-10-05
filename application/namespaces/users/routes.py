from flask_restx import Namespace, Resource
from application.namespaces.users.controllers import (
    get_user,
    post_user,
    delete_user
)
from application.namespaces.users.exceptions import (
    OrodhaBadIdError,
    OrodhaBadRequestError,
    OrodhaNotFoundError
)

user_ns = Namespace(
    "users",
    description='User related operations',
    path="/user"
)

def get_token_from_header(headers):
    """
    Accepts a request header and gets the auth token from it.

    Args:
        headers(request.headers): A dictionary containing information including our JWT token.

    Returns:
        token(str): Our token string which can be decoded via keycloak to get our user info.
    """
    token = headers.get("Authorization", "").lstrip("Bearer").strip()
    return token

@user_ns.route('/')
class UserApi(Resource):
    """
    Class that contains routes for GET, POST, and DELETE requests
    that are sent to the user namespace via /user/
    """
    def get(self):
        """
        Method which gets a user from the access token in the headers

        Returns:
            user_data(dict): The user data from our database that
                is associated with the token given to route.
        """
        try:
            request_token = get_token_from_header(user_ns.payload.headers)
            user_data = get_user(request_token)
            return user_data
        except (
            OrodhaBadIdError,
            OrodhaNotFoundError
        ) as err:
            user_ns.abort(err.status_code, err.message)

    def post(self):
        """
        Method which adds a user to keycloak and our database using form data from the request.

        Returns:
            user_data(dict): The user data for the new user created.
        """
        try:
            user_data = post_user(user_ns.payload)
            return user_data
        except OrodhaBadRequestError as err:
            user_ns.abort(err.status_code, err.message)

    def delete(self):
        """
        Method which deletes a given user from keycloak and our database
        using the access token from keycloak.

        Returns:
            deleted_id(str): The id of the deleted user
        """
        try:
            request_token = get_token_from_header(user_ns.payload.headers)
            deleted_id = delete_user(request_token)
            return deleted_id
        except (
            OrodhaNotFoundError,
            OrodhaBadRequestError
        ) as err:
            user_ns.abort(err.status_code, err.message)
