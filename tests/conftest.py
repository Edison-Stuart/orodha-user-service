import pytest
from application import create_app

@pytest.fixture
def mock_app_client():
    app = create_app()
    yield app.test_client()
