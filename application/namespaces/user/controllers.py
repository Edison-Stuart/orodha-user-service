import orodha_keycloak
from application.config import obtain_config
from application.namespaces.user.models import User
from keycloak import KeycloakGetError
from mongoengine import (
    MultipleObjectsReturned,
    ValidationError,
    FieldDoesNotExist,
    DoesNotExist,
    OperationError,
)
from application.namespaces.user.exceptions import (
    OrodhaBadIdError,
    OrodhaBadRequestError,
    OrodhaNotFoundError,
    OrodhaForbiddenError,
)

APPCONFIG = obtain_config()


def _add_user_to_database(user_args):
    """
    Helper function which takes user_args and creates a mongo user.

    Args:
        user_args(dict): A dictionary of our user's data such as
            username and email.
    """
    return User(**user_args).save()


def _create_keycloak_client():
    """
    Helper function which creates our keycloak client from config data
    for use in our main controller functions.

    Returns:
        OrodhaKeycloakClient: A facade client used by Orodha in order to make interactions with
            keycloak more uniform for the service.
    """
    return orodha_keycloak.OrodhaKeycloakClient(
        server_url=APPCONFIG["keycloak_config"]["keycloak_server_url"],
        realm_name=APPCONFIG["keycloak_config"]["keycloak_realm_name"],
        client_id=APPCONFIG["keycloak_config"]["keycloak_client_id"],
        client_secret_key=APPCONFIG["keycloak_config"]["keycloak_client_secret_key"],
    )


def get_user(token, request_user_mongo_id):
    """
    Function that takes a token and finds the user if any in our database associated with it.

    Args:
        token(str): The token passed from the UserApi route which helps us identify user auth level.
        request_user_mongo_id(str): The user id that is associated with the user that we want to get.

    Returns:
        user(dict): A dictionary containing the data of the requested user.

    Raises:
        OrodhaForbiddenError: If the user_id passed does not match the user_id in the token.
        OrodhaBadIdError: If there is a problem with the KeycloakGet method, typically because of
            a bad id passed in.
        OrodhaNotFoundError: If there are either no matching objects in the mongo db, or if there
            are more than one object that match the same id.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_id_from_token = keycloak_client.get_user(token=token)
        keycloak_id_from_token = keycloak_id_from_token.get("id")

        user = User.objects.get(keycloak_id=keycloak_id_from_token)

        if user.mongo_id != request_user_mongo_id:
            raise OrodhaForbiddenError(
                message="You don't have permission to access this resource"
            )

        return user

    except KeycloakGetError as err:
        raise OrodhaBadIdError(err.message)
    except (MultipleObjectsReturned, DoesNotExist) as err:
        raise OrodhaNotFoundError(
            f"Unable to find unique user with userId {request_user_mongo_id}: {err}"
        )


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
        keycloak_user_data = keycloak_client.add_user(
             email=payload.get("email"),
             username=payload.get("username"),
             firstName=payload.get("firstName"),
             lastName=payload.get("lastName"),
             password=payload.get("password"),
        )
        if payload.get("mongo_id") is None:
            user_dict = {
                "email": payload.get("email"),
                "username": payload.get("username"),
                "firstName": payload.get("firstName"),
                "lastName": payload.get("lastName"),
                "keycloak_id": keycloak_user_data["id"],
            }
        else:
            user_dict = {
                "email": payload.get("email"),
                "username": payload.get("username"),
                "firstName": payload.get("firstName"),
                "lastName": payload.get("lastName"),
                "keycloak_id": keycloak_user_data["id"],
                "mongo_id": payload.get("mongo_id")
            }
        user = _add_user_to_database(user_dict)
        return user

    except (
        ValidationError,
        FieldDoesNotExist,
    ) as err:
        raise OrodhaBadRequestError(err.message)


def delete_user(token, request_user_mongo_id):
    """
    Function which deletes a given user from our database and from keycloak.

    Args:
        token(str): The token passed from the UserApi route which helps us identify user auth level.
        request_user_mongo_id(str): The user id that is associated with the user that we want to delete.

    Returns:
        request_user_mongo_id(str): The user_id of the now deleted user.

    Raises:
        OrodhaForbiddenError: If the user_id passed does not match the user_id in the token.
        OrodhaBadRequestError: If there is a validation or operation error from mongoengine.
        OrodhaNotFoundError: If there are either no matching objects in the mongo db, or if there
            are more than one object that match the same id.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_id_from_token = keycloak_client.get_user(token=token)
        keycloak_id_from_token = keycloak_id_from_token.get("id")

        user = User.objects.get(keycloak_id=keycloak_id_from_token)

        if user.mongo_id != request_user_mongo_id:
            raise OrodhaForbiddenError(
                message="You don't have permission to access this resource"
            )

        user.delete()
        keycloak_client.delete_user(keycloak_id_from_token)

        return request_user_mongo_id
    except DoesNotExist as err:
        raise OrodhaNotFoundError(
            f"Unable to find unique user with userId {request_user_mongo_id}: {err}"
        )
    except (ValidationError, OperationError) as err:
        raise OrodhaBadRequestError(f"Unable to delete User {request_user_mongo_id}: {err}")
