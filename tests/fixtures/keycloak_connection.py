"""Module which contains constant test data related to certain keycloak connection requests."""

import uuid

TEST_KEYCLOAK_USER_ID = uuid.uuid4()
TEST_USERNAME_ONE = "someuser"
TEST_USERNAME_TWO = "oneuser"

"""
Mock token values to be added as headers in certain requests.
Causes MockOrodhaKeycloakClient to fail in certain ways for testing.
"""
KEYCLOAK_FAIL_TOKEN = "fail_get"
KEYCLOAK_DOES_NOT_EXIST_TOKEN = "keycloak_does_not_exist"
MONGO_DOES_NOT_EXIST_TOKEN = "mongo_does_not_exist"
MONGO_VALIDATION_ERROR_TOKEN = "mongo_validation_error"


KEYCLOAK_BAD_ID_GET_USER_RESPONSE = {
    'id': f"{TEST_KEYCLOAK_USER_ID}50502", 'createdTimestamp': 1695143223350,
    'username': 'someuser', 'enabled': True, 'totp': False,
    'emailVerified': False, 'disableableCredentialTypes': [],
    'requiredActions': [], 'notBefore': 0,
    'access': {
        'manageGroupMembership': True,
        'view': True, 'mapRoles': True,
        'impersonate': True, 'manage': True
    }
}

KEYCLOAK_GET_USER_RESPONSE = {
    'id': str(TEST_KEYCLOAK_USER_ID), 'createdTimestamp': 1695143223350,
    'username': 'someuser', 'enabled': True, 'totp': False,
    'emailVerified': False, 'disableableCredentialTypes': [],
    'requiredActions': [], 'notBefore': 0,
    'access': {
        'manageGroupMembership': True,
        'view': True, 'mapRoles': True,
        'impersonate': True, 'manage': True
    }
}

KEYCLOAK_ADD_USER_RESPONSE = str(TEST_KEYCLOAK_USER_ID)

KEYCLOAK_DELETE_USER_RESPONSE = {}


MOCK_MONGO_USER_INPUT = {
    "email": "someemail@mail.com",
    "username": TEST_USERNAME_ONE,
    "firstName": "some",
    "lastName": "user",
    "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
}

MOCK_MONGO_USER_INPUT_TWO = {
    "email": "someemail@mail.com",
    "username": TEST_USERNAME_TWO,
    "firstName": "one",
    "lastName": "user",
    "keycloak_id": f"{str(TEST_KEYCLOAK_USER_ID)}80085",
}

GET_USER_ROUTE_RESPONSE = {
    "email": "someemail@mail.com",
    "username": TEST_USERNAME_ONE,
    "firstName": "some",
    "lastName": "user",
    "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
}

BULK_GET_USER_REQUEST = {
    "pageSize": 10,
    "pageNumber": 1,
    "targets": [TEST_USERNAME_ONE, TEST_USERNAME_TWO]
    }

POST_USER_REQUEST = {
    "email": "someemail@mail.com",
    "username": TEST_USERNAME_ONE,
    "firstName": "some",
    "lastName": "user",
    "password": "somepassword",
}

POST_USER_ROUTE_RESPONSE = {
    "email": "someemail@mail.com",
    "username": TEST_USERNAME_ONE,
    "firstName": "some",
    "lastName": "user",
    "keycloak_id": str(TEST_KEYCLOAK_USER_ID),
}

POST_USER_REQUEST_INVALID = {
    "email": 23,
    "username": None,
    "password": True
}
