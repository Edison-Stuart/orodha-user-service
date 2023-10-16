# pylint: disable=no-self-use
"""
Module which contains the flask restx routes for the user service api.
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from application.namespaces.user.exceptions import (
    OrodhaBadIdError,
    OrodhaBadRequestError,
    OrodhaNotFoundError,
    OrodhaForbiddenError,
)
import application.namespaces.user.controllers

user_ns = Namespace("users", description="User related operations")

user_creation_model = user_ns.model(
    "User Input",
    {
        "email": fields.String(required=False),
        "mongo_id": fields.String(required=False),
        "username": fields.String(required=True),
        "firstName": fields.String(required=True),
        "lastName": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

user_response_model = user_ns.model(
    "User Response",
    {
        "mongo_id": fields.String(required=True),
        "keycloak_id": fields.String(required=False),
        "email": fields.String(required=False),
        "username": fields.String(required=True),
        "firstName": fields.String(required=True),
        "lastName": fields.String(required=True),
    },
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


@user_ns.route("")
class UsersApi(Resource):
    """
    Class that contains a route for the POST request
    that is sent to the user namespace via /user
    """

    @user_ns.expect(user_creation_model, validate=True)
    @user_ns.marshal_with(user_response_model)
    def post(self):
        """
        Method which adds a user to keycloak and our database using form data from the request.

        Returns:
            user_data(dict): The user data for the new user created.
        """
        try:
            user_data = application.namespaces.user.controllers.post_user(
                user_ns.payload
            )
        except OrodhaBadRequestError as err:
            user_ns.abort(err.status_code, err.message)

        return user_data


@user_ns.route("/<mongo_user_id>")
class UserApi(Resource):
    """
    Class that contains routes for GET, POST, and DELETE requests
    that are sent to the user namespace via /user/
    """

    @user_ns.marshal_with(user_response_model)
    def get(self, mongo_user_id):
        """
        Method which gets a user from the access token in the headers

        Args:
            mongo_user_id(str): The user_id passed into our route and we are targeting to get

        Returns:
            user_data(dict): The user data from our database that
                is associated with the token given to route.
        """
        try:
            request_token = get_token_from_header(request.headers)
            user_data = application.namespaces.user.controllers.get_user(
                request_token, mongo_user_id
            )
        except (
            OrodhaNotFoundError,
            OrodhaBadIdError,
            OrodhaForbiddenError,
        ) as err:
            user_ns.abort(err.status_code, err.message)

        return user_data

    def delete(self, mongo_user_id):
        """
        Method which deletes a given user from keycloak and our database
        using the access token from keycloak.

        Args:
            mongo_user_id(str): The user_id passed into our route and we are targeting for deletion.

        Returns:
            deleted_id(str): The id of the deleted user
        """
        try:
            request_token = get_token_from_header(request.headers)
            deleted_id = application.namespaces.user.controllers.delete_user(
                request_token, mongo_user_id
            )
        except (
            OrodhaNotFoundError,
            OrodhaBadRequestError,
            OrodhaForbiddenError,
        ) as err:
            user_ns.abort(err.status_code, err.message)

        return deleted_id
