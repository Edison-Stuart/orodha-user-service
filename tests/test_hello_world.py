import pytest

def test_get_main_namespace(mock_app_client):    
    json_response = mock_app_client.get(
    "/api/v1/main/hello"
	)
    assert json_response.status_code == 200
