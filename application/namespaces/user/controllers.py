"""
Module that contains the controller or 'Business Logic' functions which interact with
our storage and user auth services for our routes.
"""
import orodha_keycloak
from keycloak import KeycloakGetError
from mongoengine import (
    MultipleObjectsReturned,
    ValidationError,
    FieldDoesNotExist,
    DoesNotExist,
    OperationError,
)
from application.config import obtain_config
from application.namespaces.user.common import pipelines
from application.namespaces.user.models import User
from application.namespaces.user.exceptions import (
    OrodhaBadIdError,
    OrodhaBadRequestError,
    OrodhaNotFoundError,
    OrodhaForbiddenError,
)

APPCONFIG = obtain_config()
DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


def _add_user_to_database(user_args: dict) -> User:
    """
    Helper function which takes user_args and creates a mongo user.

    Args:
        user_args(dict): A dictionary of our user's data such as
            username and email.

    Returns:
        User: The user Document blueprint that is defined in models.py,
            filled with data from user_args
    """
    return User(**user_args).save()


def _create_keycloak_client() -> orodha_keycloak.OrodhaKeycloakClient:
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


def get_bulk_users(token: str, payload: dict) -> list:
    """
    Function that takes a JWT and optional filters, then returns truncated user data.

    Args:
        token(str): A JWT token provided by keycloak.
        payload(dict): The post payload containing filter data and user data

    Raises:
        OrodhaForbidenError: If the JWT token is not valid or is missing.

    Returns:
        response_data(list[UserDocument]): A list of matching user documents that have been trimmed
            to the id and username values only.
    """
    keycloak_client = _create_keycloak_client()

    try:
        keycloak_client.get_user(token=token).get("id")
    except KeycloakGetError:
        raise OrodhaForbiddenError(
            message="You don't have the required token to access this resource."
        )

    page_size = int(payload.get("pageSize", DEFAULT_PAGE_SIZE))
    page_number = int(payload.get("pageNumber", DEFAULT_PAGE_NUMBER))

    if page_number == 1:
        offset = 0
    else:
        offset = (page_size * page_number) - page_size

    bulk_user_pipeline = pipelines.obtain_bulk_user_pipeline(
        page_size=page_size,
        offset=offset,
        targets=payload.get("targets")
    )
    response_data = User.objects().aggregate(bulk_user_pipeline)
    return list(response_data)


def get_user(token: str, request_user_mongo_id: str) -> User:
    """
    Function that takes a token and finds the user if any in our database associated with it.

    Args:
        token(str): The token passed from the UserApi route which helps us identify user auth level.
        request_user_mongo_id(str): The user id that is associated with the user that we want to get.

    Returns:
        user(document): A mongoengine document object containing the data of the requested user.

    Raises:
        OrodhaBadIdError: If there is a problem with the KeycloakGet method, typically because of
            a bad id passed in.
        OrodhaNotFoundError: If there are either no matching objects in the mongo db, or if there
            are more than one object that match the same id.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_id_from_token = keycloak_client.get_user(token=token).get("id")

        user = User.objects.get(keycloak_id=keycloak_id_from_token)

        if str(user.id) != request_user_mongo_id:
            raise OrodhaForbiddenError(
                message="You don't have permission to access this resource"
            )

        return user

    except KeycloakGetError as err:
        raise OrodhaBadIdError(
            f"Unable to find keycloak user with token {token}: {err}"
        )
    except (MultipleObjectsReturned, DoesNotExist) as err:
        raise OrodhaNotFoundError(
            f"Unable to find unique user with userId {request_user_mongo_id}: {err}"
        )


def post_user(payload: dict) -> User:
    """
    Function which creates a new keycloak user and a new database entry from user_data.

    Args:
        payload(dict): The dictionary of arguments that was
            sent in via body data from our post route.

    Returns:
        user(document): A mongoengine document object containing the data of the created user.

    Raises:
        OrodhaBadRequestError: If there is a problem with the user document creation such as
            necessary fields missing or an internal mongoengine validation error.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_user_id = keycloak_client.add_user(
             email=payload.get("email"),
             username=payload.get("username"),
             firstName=payload.get("firstName"),
             lastName=payload.get("lastName"),
             password=payload.get("password"),
        )
        user_dict = {
            "email": payload.get("email"),
            "username": payload.get("username"),
            "firstName": payload.get("firstName"),
            "lastName": payload.get("lastName"),
            "keycloak_id": keycloak_user_id,
        }

        user = _add_user_to_database(user_dict)
        return user

    except (
        ValidationError,
        FieldDoesNotExist,
    ) as err:
        raise OrodhaBadRequestError(
            f"There was an issue creating user: {err}"
        )


def delete_user(token: str, request_user_mongo_id: str) -> str:
    """
    Function which deletes a given user from our database and from keycloak.

    Args:
        token(str): The token passed from the UserApi route which helps us identify user auth level.
        request_user_mongo_id(str): The user id that is associated with the user that we want
            to delete.

    Returns:
        request_user_mongo_id(str): The user_id of the now deleted user.

    Raises:
        OrodhaBadRequestError: If there is a validation or operation error from mongoengine.
        OrodhaNotFoundError: If there are either no matching objects in the mongo db, or if there
            are more than one object that match the same id.
    """
    try:
        keycloak_client = _create_keycloak_client()
        keycloak_id_from_token = keycloak_client.get_user(token=token)
        keycloak_id_from_token = keycloak_id_from_token.get("id")

        user = User.objects.get(keycloak_id=keycloak_id_from_token)

        if str(user.id) != request_user_mongo_id:
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
