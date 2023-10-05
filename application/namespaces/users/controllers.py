from orodha_keycloak import OrodhaKeycloakClient
from application.config import obtain_config
from application.namespaces.users.models import User
from keycloak import KeycloakGetError
from mongoengine import LookUpError as MongoLookupError
from mongoengine import (
    MultipleObjectsReturned,
    ValidationError,
    FieldDoesNotExist,
    DoesNotExist,
    OperationError
)
from application.namespaces.users.exceptions import (
    OrodhaBadIdError,
    OrodhaBadRequestError,
    OrodhaNotFoundError
)

APPCONFIG = obtain_config()

def _add_user_to_database(user_args):
    """
    Helper function which takes user_args and creates a mongo user.

    Args:
        user_args(dict): A dictionary of our user's data such as
            username and email.
    """
    User(**user_args).save()

def _delete_user_from_database(user_id):
    """
    Helper function which removes a given user from
    the mongo database using the user_id.

    Args:
        user_id(str): Can either be a keycloak_id or the objects mongo id but is connected
            to user we want to delete.
    """
    User.objects.get(id=user_id).delete()

def _create_keycloak_client():
    """
    Helper function which creates our keycloak client from config data
    for use in our main controller functions.

    Returns:
        OrodhaKeycloakClient: A facade client used by Orodha in order to make interactions with
            keycloak more uniform for the service.
    """
    return OrodhaKeycloakClient(
        server_url=APPCONFIG["keycloak_config"]["keycloak_server_url"],
        realm_name=APPCONFIG["keycloak_config"]["keycloak_realm_name"],
        client_id=APPCONFIG["keycloak_config"]["keycloak_client_id"],
        client_secret_key=APPCONFIG["keycloak_config"]["keycloak_client_secret_key"]
    )

def get_user(token):
    """
    Function that takes a token and finds the user if any in our database associated with it.

    Args:
        token(str): The keycloak token obtained from the headers of the get request.

    Returns:
        user(dict): A dictionary containing the data of the requested user.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_user = keycloak_client.get_user(token=token)
        user = User.objects.get(keycloak_id=keycloak_user.get("id"))
        return user
    except (
        KeycloakGetError,
    ) as err:
        raise OrodhaBadIdError(err.message)
    except (
        MultipleObjectsReturned,
        DoesNotExist
    ) as err:
        raise OrodhaNotFoundError(err.message)

def post_user(payload):
    """
    Funtion which creates a new keycloak user and a new database entry from user_data.

    Args:
        payload(dict): The dictionary of arguments that was
            sent in via body data from our post route.

    Returns:
        user_dict(dict): A dictionary containing the data of the new user that was created.
    """
    try:
        keycloak_client = _create_keycloak_client()

        user_id = keycloak_client.add_user(
            email=payload.get("email"),
            username=payload.get("username"),
            firstName=payload.get("firstName"),
            lastName=payload.get("lastName"),
            password=payload.get("password")
        )
        user_dict = {
            "email": payload.get("email"),
            "username": payload.get("username"),
            "firstName": payload.get("firstName"),
            "lastName": payload.get("lastName"),
            "keycloak_id": user_id
        }
        _add_user_to_database(user_dict)

        return user_dict
    except (
        ValidationError,
        FieldDoesNotExist,
    ) as err:
        raise OrodhaBadRequestError(message=err.message)

def delete_user(token):
    """
    Function which deletes a given user from our database and from keycloak.

    Args:
        token(str): The keycloak token that is associated with the user that we want to delete.

    Returns:
        user_id(str): The user_id of the now deleted user.
    """
    try:
        keycloak_client = _create_keycloak_client()

        user_id = keycloak_client.get_user(token=token).get("id")
        _delete_user_from_database(user_id)
        keycloak_client.delete_user(user_id)

        return user_id
    except DoesNotExist as err:
        raise OrodhaNotFoundError(err.message)
    except (
        ValidationError,
        OperationError
    ) as err:
        raise OrodhaBadRequestError(err.message)
