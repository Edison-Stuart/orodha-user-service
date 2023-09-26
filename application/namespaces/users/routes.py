from flask_restx import Namespace, Resource
from flask import request
from orodha_keycloak import OrodhaKeycloakClient
from application.config import obtain_config
from application.namespaces.users.controllers import (
    get_user_with_token,
    post_new_user_data,
    put_user_with_token,
    delete_user_with_token
)

user_ns = Namespace(
    "users",
    description='User related operations',
    path="/user"
    )

APPCONFIG = obtain_config()

# class SomeResource(Resource):
@main_ns.route('/user')
class Users(Resource):
    def get(self):
        keycloak_client = OrodhaKeycloakClient(
            server_url=APPCONFIG.get("keycloak_server_url"),
            realm_name=APPCONFIG.get("keycloak_realm_name"),
            client_id=APPCONFIG.get("keycloak_client_id"),
            client_secret_key=APPCONFIG.get("keycloak_client_secret_key"),
         )
        request_token = request.headers.get("access_token")
        return get_user_with_token(request_token)

        return "Hello World"
    def post(self):
        keycloak_client = OrodhaKeycloakClient(
            server_url=APPCONFIG.get("keycloak_server_url"),
            realm_name=APPCONFIG.get("keycloak_realm_name"),
            client_id=APPCONFIG.get("keycloak_client_id"),
            client_secret_key=APPCONFIG.get("keycloak_client_secret_key"),
         )

    def put(self):
        keycloak_client = OrodhaKeycloakClient(
            server_url=APPCONFIG.get("keycloak_server_url"),
            realm_name=APPCONFIG.get("keycloak_realm_name"),
            client_id=APPCONFIG.get("keycloak_client_id"),
            client_secret_key=APPCONFIG.get("keycloak_client_secret_key"),
         )

    def delete(self):
        keycloak_client = OrodhaKeycloakClient(
            server_url=APPCONFIG.get("keycloak_server_url"),
            realm_name=APPCONFIG.get("keycloak_realm_name"),
            client_id=APPCONFIG.get("keycloak_client_id"),
            client_secret_key=APPCONFIG.get("keycloak_client_secret_key"),
         )
