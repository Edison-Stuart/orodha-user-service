"""Module which contains our tests for the users namespace and routes, positive and negative."""
from .fixtures import (
    GET_USER_ROUTE_RESPONSE,
    POST_USER_REQUEST,
    POST_USER_REQUEST_INVALID,
    POST_USER_ROUTE_RESPONSE,
    KEYCLOAK_FAIL_TOKEN,
    MONGO_DOES_NOT_EXIST_TOKEN,
    KEYCLOAK_DOES_NOT_EXIST_TOKEN,
    MONGO_VALIDATION_ERROR_TOKEN
)
from http import HTTPStatus
from copy import deepcopy

USER_ROUTE = "/api/v1/users"

def test_delete(mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which creates a new user and then deletes the user, looking for the
    200 status code as well as the deleted id of the user.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    mock_id = mock_user_object.id

    response_delete = mock_app_client.delete(
        f"{USER_ROUTE}/{str(mock_id)}", headers={"Content-Type": "application/json"}
    )
    assert response_delete.json == str(mock_id)
    assert response_delete.status_code == HTTPStatus.OK


def test_get(mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which requests the data of our mock user object form the server.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked version
            of the oroha-keycloak package fpr testing purposes.
    """
    mock_id = mock_user_object.id
    expected = deepcopy(GET_USER_ROUTE_RESPONSE)
    expected["id"] = str(mock_id)
    response_get = mock_app_client.get(
        f"{USER_ROUTE}/{str(mock_id)}", headers={"Content-Type": "application/json"}
    )
    assert response_get.json == expected
    assert response_get.status_code == HTTPStatus.OK


def test_get_all(mock_service_env, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which calls the user get route with no arguments,
    obtaining all user_id and keycloak_id values.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    response_get_all = mock_app_client.get(
        f"{USER_ROUTE}", headers={"Content-Type": "application/json"}
    )

    assert response_get_all.status_code == HTTPStatus.OK
    assert isinstance(response_get_all.json, list)
    assert isinstance(response_get_all.json[0], dict)
    response_keys = response_get_all.json[0].keys()
    assert len(response_keys) == 3
    assert "_id" in response_keys
    assert "keycloak_id" in response_keys
    assert "username" in response_keys


def test_post(mock_service_env, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which adds a user to the database and asserts the correct information has
    been returned.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    response_post = mock_app_client.post(
        USER_ROUTE, json=POST_USER_REQUEST
    )
    response_json = response_post.json

    email = POST_USER_ROUTE_RESPONSE["email"]
    username = POST_USER_ROUTE_RESPONSE["username"]
    firstName = POST_USER_ROUTE_RESPONSE["firstName"]
    lastName = POST_USER_ROUTE_RESPONSE["lastName"]
    keycloak_id = POST_USER_ROUTE_RESPONSE["keycloak_id"]

    assert response_post.status_code == HTTPStatus.OK

    assert response_json["email"] == email
    assert response_json["username"] == username
    assert response_json["firstName"] == firstName
    assert response_json["lastName"] == lastName
    assert response_json["keycloak_id"] == keycloak_id
    assert response_json["id"] is not None


def test_get_keycloak_error(mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which purposely throws a keycloak error from our get controller function then
    checks to see if our routes properly caught the exception.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.

    """
    mock_id = mock_user_object.id
    response_get = mock_app_client.get(
        f"{USER_ROUTE}/{str(mock_id)}", headers={
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {KEYCLOAK_FAIL_TOKEN}"
        }
    )
    assert response_get.status_code == HTTPStatus.BAD_REQUEST


def test_get_mongo_error(mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection):
    """
    Test function which purposely throws a mongoengine error from our get controller function then
    checks to see if our routes properly caught the exception.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    mock_id = mock_user_object.id
    response_get = mock_app_client.get(
        f"{USER_ROUTE}/{str(mock_id)}", headers={
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {MONGO_DOES_NOT_EXIST_TOKEN}"
        })
    assert response_get.status_code == HTTPStatus.NOT_FOUND


def test_post_mongo_error(
    mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection
):
    """
    Test function which purposely throws a keycloak error from our post controller function then
    checks to see if our routes properly caught the exception.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    response_post = mock_app_client.post(
        USER_ROUTE, json=POST_USER_REQUEST_INVALID
    )
    assert response_post.status_code == HTTPStatus.BAD_REQUEST


def test_delete_does_not_exist(
    mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection
):
    """
    Test function which purposely throws a mongo error from our delete controller function then
    checks to see if our routes properly caught the exception.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    mock_id = mock_user_object.id
    response_delete = mock_app_client.delete(f"{USER_ROUTE}/{str(mock_id)}", headers={
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {KEYCLOAK_DOES_NOT_EXIST_TOKEN}"
        })
    assert response_delete.status_code == HTTPStatus.NOT_FOUND


def test_delete_validation_error(
    mock_service_env, mock_user_object, mock_app_client, mock_create_keycloak_connection
):
    """
    Test function which purposely throws a mongo validation error from our get controller
    function then checks to see if our routes properly caught the exception.

    Args:
        mock_service_env: A fixture function which loads the service environment with
            variables from fixture data.
        mock_user_object: A fixture function which creates and returns a custom mongo document user
            object for us to test with.
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_create_keycloak_connection: Fixture function which returns to us a mocked
            version of the oroha-keycloak package fpr testing purposes.
    """
    mock_id = mock_user_object.id
    response_delete = mock_app_client.delete(
        f"{USER_ROUTE}/{str(mock_id)}", headers={
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {MONGO_VALIDATION_ERROR_TOKEN}"
        }
    )
    assert response_delete.status_code == HTTPStatus.BAD_REQUEST
