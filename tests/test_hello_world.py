"""Module which tests our main namespace route for health."""
def test_get_main_namespace(mock_service_env, mock_app_client):
    json_response = mock_app_client.get("/api/v1/main/hello")
    assert json_response.status_code == 200
