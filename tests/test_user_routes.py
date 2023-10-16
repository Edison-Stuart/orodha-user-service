from .fixtures import MOCK_DATA, TEST_MONGO_USER_ID, TEST_KEYCLOAK_USER_ID
from http import HTTPStatus

USER_ROUTE = "/api/v1/users"


# def test_get(mock_service_env, create_mock_user_object, mock_app_client, mock_create_keycloak_connection):
#     """
#     Test function which first posts to the mock db, then requests the data back.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_create_keycloak_connection: Fixture function which returns to us a mocked version
#             of the oroha-keycloak package fpr testing purposes.
#     """
#     mock_id = create_mock_user_object.mongo_id
#     response_get = mock_app_client.get(
#         f"{USER_ROUTE}/{mock_id}", headers={"Content-Type": "application/json"}
#     )
#     assert response_get.json == MOCK_DATA["get_user_route_response"]
#     assert response_get.status_code == HTTPStatus.OK


# def test_post(mock_service_env, mock_app_client, mock_create_keycloak_connection):
#     """
#     Test function which adds a user to the database and asserts the correct information has
#     been returned.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_create_keycloak_connection: Fixture function which returns to us a mocked
#             version of the oroha-keycloak package fpr testing purposes.
#     """
#     response_post = mock_app_client.post(
#         USER_ROUTE, json=MOCK_DATA["post_user_request"]
#     )
#     assert response_post.json == MOCK_DATA["post_user_route_response"]
#     assert response_post.status_code == HTTPStatus.OK


# def test_delete(mock_service_env, create_mock_user_object, mock_app_client, mock_create_keycloak_connection):
#     """
#     Test function which creates a new user and then deletes the user, looking for the
#     200 status code.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_create_keycloak_connection: Fixture function which returns to us a mocked
#             version of the oroha-keycloak package fpr testing purposes.
#     """
#     post_user_response = mock_app_client.post(
#         USER_ROUTE, json=MOCK_DATA["post_user_request"]
#     )
#     user_data = post_user_response.json
#     response_delete = mock_app_client.delete(
#         f"{USER_ROUTE}/{user_data['mongo_id']}", headers={"Content-Type": "application/json"}
#     )
#     assert response_delete.text == ""
#     assert response_delete.status_code == HTTPStatus.OK


def test_get_keycloak_error(mock_service_env, create_mock_user_object, mock_app_client, mock_get_keycloak_error):
    """
    Test function which purposely throws a keycloak error from our get controller function then
    checks to see if our routes properly caught the exception.

    Args:
        mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
            connection.
        mock_get_keycloak_error: A fixture function which creates the side effect of a
            specific error that we want our route to catch.
    """
    response_get = mock_app_client.get(f"{USER_ROUTE}/{TEST_MONGO_USER_ID}", headers={"Content-Type": "application/json"})
    assert response_get.status_code == HTTPStatus.BAD_REQUEST


# def test_get_mongo_error(mock_service_env, create_mock_user_object, mock_app_client, mock_get_mongo_error):
#     """
#     Test function which purposely throws a mongoengine error from our get controller function then
#     checks to see if our routes properly caught the exception.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_get_mongo_error: A fixture function which creates the side effect of a
#             specific error that we want our route to catch.
#     """
#     response_get = mock_app_client.get(USER_ROUTE, follow_redirects=True)
#     assert response_get.status_code == HTTPStatus.NOT_FOUND


# def test_post_keycloak_error(
#     mock_service_env, create_mock_user_object, mock_app_client, mock_post_keycloak_error
# ):
#     """
#     Test function which purposely throws a keycloak error from our post controller function then
#     checks to see if our routes properly caught the exception.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_post_keycloak_error: A fixture function which creates the side effect of a
#             specific error that we want our route to catch.
#     """
#     response_post = mock_app_client.post(
#         USER_ROUTE, follow_redirects=True, data=MOCK_DATA["post_user_request"]
#     )
#     assert response_post.status_code == HTTPStatus.BAD_REQUEST


# def test_delete_does_not_exist(
#     mock_service_env, create_mock_user_object, mock_app_client, mock_delete_does_not_exist
# ):
#     """
#     Test function which purposely throws a mongo error from our delete controller function then
#     checks to see if our routes properly caught the exception.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_delete_does_not_exist: A fixture function which creates the side effect of a specific
#             error being thrown for our route to catch.
#     """
#     mock_app_client.post(
#         USER_ROUTE, follow_redirects=True, data=MOCK_DATA["post_user_request"]
#     )
#     response_get = mock_app_client.delete(ROUTE_WITH_ID, follow_redirects=True)
#     assert response_get.status_code == HTTPStatus.NOT_FOUND


# def test_delete_validation_error(
#     mock_service_env, create_mock_user_object, mock_app_client, mock_delete_validation_error
# ):
#     """
#     Test function which purposely throws a mongo validation error from our get controller
#     function then checks to see if our routes properly caught the exception.

#     Args:
#         mock_app_client: An instance of our Flask app which has been loaded with a MongoMock
#             connection.
#         mock_delete_validation_error: A fixture function which creates the side effect of a specific
#             error being thrown for our route to catch.
#     """
#     mock_app_client.post(
#         USER_ROUTE, follow_redirects=True, data=MOCK_DATA["post_user_request"]
#     )
#     response_delete = mock_app_client.delete(
#         ROUTE_WITH_ID,
#         follow_redirects=True,
#     )
#     assert response_delete.status_code == HTTPStatus.BAD_REQUEST
