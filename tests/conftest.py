"""Module which contains fixture functions that aid in testing our routes and controllers."""
import os
import pytest
from keycloak import KeycloakGetError
from application import create_base_app
from application.namespaces.user.models import User
from .fixtures import (
    MOCK_MONGO_USER_INPUT,
    TEST_ENVIRONMENT,
    KEYCLOAK_ADD_USER_RESPONSE,
    KEYCLOAK_DELETE_USER_RESPONSE,
    KEYCLOAK_GET_USER_RESPONSE,
    KEYCLOAK_FAIL_TOKEN,
    MONGO_DOES_NOT_EXIST_TOKEN,
    KEYCLOAK_BAD_ID_GET_USER_RESPONSE,
    KEYCLOAK_DOES_NOT_EXIST_TOKEN,
    MONGO_VALIDATION_ERROR_TOKEN,
    MOCK_MONGO_USER_INPUT_TWO
)
from mongoengine import DoesNotExist, ValidationError, connect
import mongomock


@pytest.fixture
def mock_app_client():
    app = create_base_app()
    connect(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()



@pytest.fixture
def mock_user_object():
    mock_user = User(**MOCK_MONGO_USER_INPUT)
    mock_user.save()
    yield mock_user

@pytest.fixture
def mock_user_object_two():
    mock_user = User(**MOCK_MONGO_USER_INPUT_TWO)
    mock_user.save()
    yield mock_user

@pytest.fixture()
def mock_service_env():
    os.environ.update(TEST_ENVIRONMENT)


class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""

    def add_user(self, *args, **kwargs):
        return KEYCLOAK_ADD_USER_RESPONSE

    def delete_user(self, *args, **kwargs):
        return KEYCLOAK_DELETE_USER_RESPONSE

    def get_user(self, *args, **kwargs):
        if kwargs.get("token") == KEYCLOAK_FAIL_TOKEN:
            raise KeycloakGetError()
        elif kwargs.get("token") == KEYCLOAK_DOES_NOT_EXIST_TOKEN:
            raise DoesNotExist()
        elif kwargs.get("token") == MONGO_VALIDATION_ERROR_TOKEN:
            raise ValidationError()
        elif kwargs.get("token") == MONGO_DOES_NOT_EXIST_TOKEN:
            return KEYCLOAK_BAD_ID_GET_USER_RESPONSE
        else:
            return KEYCLOAK_GET_USER_RESPONSE


@pytest.fixture
def mock_create_keycloak_connection(mocker):
    """
    Fixture which patches our create_client_connection function to return our mocked client.
    """
    mocker.patch(
        "application.namespaces.user.controllers._create_keycloak_client",
        return_value=MockOrodhaKeycloakClient(),
    )
