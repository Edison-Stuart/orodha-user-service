import pytest
from application import create_base_app
from application.namespaces.users.db import get_db_connection
from .fixtures import MOCK_DATA
import mongomock

class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""
    def add_user(self,*user_info):
        return MOCK_DATA["add_user_response"]
    def delete_user(self, user_id):
        return MOCK_DATA["delete_user_response"]
    def get_user(self, token: str = None, user_id: str = None):
        return MOCK_DATA["get_user_response"]
    def decode_jwt(self, token):
        return MOCK_DATA["decode_jwt_response"]

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
def mock_app_client():
    app = create_base_app()
    get_db_connection(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()
