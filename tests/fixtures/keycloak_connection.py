"""Module which contains constant test data related to certain keycloak connection requests"""

from bson.objectid import ObjectId

TEST_KEYCLOAK_USER_ID = ObjectId()
TEST_MONGO_USER_ID = ObjectId()

MOCK_DATA = {
    "get_user_route_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
        "mongo_id": str(TEST_MONGO_USER_ID)
    },
    "post_user_route_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
        "mongo_id": str(TEST_MONGO_USER_ID)
    },
    "add_user_keycloak_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "id": str(TEST_KEYCLOAK_USER_ID),
    },
    "post_user_request": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "password": "somepassword",
        "mongo_id": str(TEST_MONGO_USER_ID)
    },
    "delete_user_response": "",
    "decode_jwt_response": {
        "email": "someemail@mail.com",
        "username": "someuser",
        "firstName": "some",
        "lastName": "user",
        "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
        "mongo_id": str(TEST_MONGO_USER_ID)
    },
}
