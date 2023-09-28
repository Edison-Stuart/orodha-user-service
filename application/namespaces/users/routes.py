from flask_restx import Namespace, Resource
from application.config import obtain_config
from application.namespaces.users.controllers import (
    get_user,
    post_user,
    delete_user
)

user_ns = Namespace(
    "users",
    description='User related operations',
    path="/user"
)

APPCONFIG = obtain_config()

def get_token_from_header(header):
    """
    Accepts a request header and gets the auth token from it.

    Args:
        header(request.headers): A dictionary containing information including our JWT token.

    Returns:
        token(str): Our token string which can be decoded via keycloak to get our user info.
    """
    token = header.get("Authorization", "").lstrip("Bearer").strip()
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
        unstripped_token = user_ns.payload.headers["access_token"]
        request_token = get_token_from_header(unstripped_token)
        user_data = get_user(request_token)
        return user_data

    def post(self):
        """
        Method which adds a user to keycloak and our database using form data from the request.

        Returns:
            user_data(dict): The user data for the new user created.
        """
        user_data = post_user(user_ns.payload)
        return user_data

    def delete(self):
        """
        Method which deletes a given user from keycloak and our database
        using the access token from keycloak.

        Returns:
            deleted_id(str): The id of the deleted user
        """
        unstripped_token = user_ns.payload.headers["access_token"]
        request_token = get_token_from_header(unstripped_token)
        deleted_id = delete_user(request_token)
        return deleted_id
