from .keycloak_connection import *


TEST_ENVIRONMENT = {
    "KEYCLOAK_SERVER_URL": "keycloak:8080/auth/",
    "KEYCLOAK_REALM_NAME": "user",
    "KEYCLOAK_CLIENT_ID": "user_client",
    "KEYCLOAK_CLIENT_SECRET_KEY": "some_secret",
    "DBUSER": "dbuser",
    "DBPASSWORD": "somepassword",
    "DBPORTS": "27017:27017",
    "DBHOSTNAME": "user-service-mongo",
    "DBROOTUSER": "rootdbuser",
    "DBROOTPASSWORD": "rootdbpassword",
    "DBNAME": "budget-generator",
    "DB_DATABASE": "keycloakdb",
    "DB_ADDR": "keycloak-db",
    "POSTGRES_DB": "keycloakdb",
    "POSTGRES_USER": "admin",
    "POSTGRES_PASSWORD": "password",
    "KEYCLOAK_HOSTNAME": "orodha.auth",
    "EYCLOAK_USER": "admin",
    "KEYCLOAK_PASSWORD": "password",
    "DB_VENDOR": "postgres",
}
