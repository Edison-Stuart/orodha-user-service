import os
import pytest
from keycloak import KeycloakGetError
from application import create_base_app
from application.namespaces.user.models import User
from .fixtures import MOCK_DATA, TEST_ENVIRONMENT
from mongoengine import DoesNotExist, FieldDoesNotExist, ValidationError, connect
import mongomock


@pytest.fixture
def mock_app_client():
    app = create_base_app()
    connect(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()



@pytest.fixture
def create_mock_user_object():
    mock_user = User(**MOCK_DATA["decode_jwt_response"])
    mock_user.save()
    yield mock_user

@pytest.fixture()
def mock_service_env():
    os.environ.update(TEST_ENVIRONMENT)


class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""

    def add_user(self, *args, **kwargs):
        return MOCK_DATA["add_user_keycloak_response"]

    def delete_user(self, *args, **kwargs):
        return MOCK_DATA["delete_user_response"]

    def get_user(self, *args, **kwargs):
        return MOCK_DATA["get_user_route_response"]

    def decode_jwt(self, *args, **kwargs):
        return MOCK_DATA["decode_jwt_response"]


def fail_get_keycloak(*args, **kwargs):
    raise KeycloakGetError()


def fail_does_not_exist(*args, **kwargs):
    raise DoesNotExist()


def fail_field_does_not_exist(*args, **kwargs):
    raise FieldDoesNotExist()


def fail_delete_validation(*args, **kwargs):
    raise ValidationError()


@pytest.fixture
def mock_create_keycloak_connection(mocker):
    """
    Fixture which patches our create_client_connection function to return our mocked client.
    """
    mocker.patch(
        "application.namespaces.user.controllers._create_keycloak_client",
        return_value=MockOrodhaKeycloakClient(),
    )


@pytest.fixture
def mock_get_keycloak_error(mocker):
    mocker.patch(
        "application.namespaces.user.controllers.get_user",
        side_effect=fail_get_keycloak,
    )


@pytest.fixture
def mock_get_mongo_error(mocker):
    mocker.patch(
        "application.namespaces.user.controllers.get_user",
        side_effect=fail_does_not_exist,
    )


@pytest.fixture
def mock_post_keycloak_error(mocker):
    mocker.patch(
        "application.namespaces.user.controllers.post_user",
        side_effect=fail_field_does_not_exist,
    )


@pytest.fixture
def mock_delete_does_not_exist(mocker):
    mocker.patch(
        "application.namespaces.user.controllers.delete_user",
        side_effect=fail_does_not_exist,
    )


@pytest.fixture
def mock_delete_validation_error(mocker):
    mocker.patch(
        "application.namespaces.user.controllers.delete_user",
        side_effect=fail_delete_validation,
    )
