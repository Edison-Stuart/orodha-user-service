import pytest
from application import create_app
from .fixtures import MOCK_DATA

def test_get(mock_create_keycloak_connection, mock_app_client):
    response_get = mock_app_client.get(
            "/api/v1/main/users/",
            follow_redirects=True
        )
    assert response_get == MOCK_DATA["get_user_response"]

def test_post_and_delete(mock_create_keycloak_connection):
    pass
