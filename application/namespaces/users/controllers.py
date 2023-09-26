from orodha_keycloak import OrodhaKeycloakConnection
from application.config import obtain_config

APPCONFIG = obtain_config()

def get_user_with_token(token):
    keycloak_client = OrodhaKeycloakClient(
    server_url=APPCONFIG.get("keycloak_server_url"),
    realm_name=APPCONFIG.get("keycloak_realm_name"),
    client_id=APPCONFIG.get("keycloak_client_id"),
    client_secret_key=APPCONFIG.get("keycloak_client_secret_key"),
)

def post_new_user_data():
    pass

def delete_user_with_token():
    pass

def put_user_with_token():
    pass
