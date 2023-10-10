import pytest
from application.namespaces.users.exceptions import (
    OrodhaNotFoundError,
    OrodhaBadIdError,
    OrodhaBadRequestError,
)
from .fixtures import MOCK_DATA

USER_ROUTE = "/api/v1/users"

def test_get(mock_create_keycloak_connection, mock_app_client):
    response_get = mock_app_client.get(
        USER_ROUTE,
        follow_redirects=True
    )
    assert response_get.json == MOCK_DATA["get_user_route_response"]

def test_post(mock_create_keycloak_connection, mock_app_client):
    response_post = mock_app_client.post(
        USER_ROUTE,
        follow_redirects=True,
        data=MOCK_DATA["post_user_request"]
    )
    assert response_post.json == MOCK_DATA["post_user_route_response"]

# def test_get_keycloak_error(mock_app_client, mock_get_keycloak_error):
#         with pytest.raises()
#         response_get = mock_app_client.get(
#         USER_ROUTE,
#         follow_redirects=True
#     )

def test_get_mongo_error(mock_app_client, mock_get_mongo_error):
    pass

def test_post_keycloak_error(mock_app_client, mock_post_keycloak_error):
    pass

def test_delete_does_not_exist(mock_app_client, mock_delete_does_not_exist):
    pass

def test_delete_validation_error(mock_app_client, mock_delete_validation_error):
    pass
