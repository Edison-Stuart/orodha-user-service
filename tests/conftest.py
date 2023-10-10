from more_itertools import side_effect
import pytest
from keycloak import KeycloakGetError
from application import create_base_app
from application.namespaces.users.db import get_db_connection
from .fixtures import MOCK_DATA
from mongoengine import DoesNotExist, FieldDoesNotExist, ValidationError
import mongomock

class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""
    def add_user(self,*user_info):
        return MOCK_DATA["add_user_keycloak_response"]
    def delete_user(self, user_id):
        return MOCK_DATA["delete_user_response"]
    def get_user(self, token: str = None, user_id: str = None):
        return MOCK_DATA["get_user_keycloak_response"]
    def decode_jwt(self, token):
        return MOCK_DATA["decode_jwt_response"]

def fail_get_keycloak():
    raise KeycloakGetError(message="test")

def fail_does_not_exist():
    raise DoesNotExist(message="test")

def fail_post_mongo():
    raise FieldDoesNotExist(message="test")

def fail_delete_validation():
    raise ValidationError(message="test")

@pytest.fixture
def mock_create_keycloak_connection(mocker):
    """
    Fixture which patches our create_client_connection function to return our mocked client.
    """
    mocker.patch(
        "orodha_keycloak.OrodhaKeycloakClient",
        return_value=MockOrodhaKeycloakClient(),
    )

@pytest.fixture
def mock_get_keycloak_error(mocker):
    mocker.patch(
        "application.namespaces.user.controller.get_user",
        side_effect=fail_get_keycloak()
    )

@pytest.fixture
def mock_get_mongo_error(mocker):
    mocker.patch(
        "application.namespaces.user.controller.get_user",
        side_effect=fail_does_not_exist()
    )

@pytest.fixture
def mock_post_keycloak_error(mocker):
    mocker.patch(
        "application.namespaces.user.controller.post_user",
        side_effect=fail_post_mongo()
    )

@pytest.fixture
def mock_delete_does_not_exist(mocker):
    mocker.patch(
        "application.namespaces.user.controller.delete_user",
        return_value=fail_does_not_exist()
    )

@pytest.fixture
def mock_delete_validation_error(mocker):
    mocker.patch(
        "application.namespaces.user.controller.delete_user",
        return_value=fail_delete_validation()
    )

@pytest.fixture
def mock_app_client():
    app = create_base_app()
    get_db_connection(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()
