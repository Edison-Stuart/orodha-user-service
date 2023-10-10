"""Module which contains constant test data related to certain keycloak connection requests"""
MOCK_DATA = {
    "get_user_keycloak_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "keycloak_id": "someuserid"
        },
    "post_user_keycloak_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "keycloak_id": "some_user_id"
    },
    "get_user_route_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "id": "some_user_id"
        },
    "post_user_route_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "id": "some_user_id"
    },
    "post_user_request": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "password": "somepassword"
        },
    "delete_user_response": "",
    "decode_jwt_response": {"id": "someuserid"}
}
