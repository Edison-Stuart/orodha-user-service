"""
Contains OrodhaErrors which are thrown by the user routes.
"""
from http import HTTPStatus

class OrodhaForbiddenError(Exception):
    """
    Exception for when a request is made with a mis-matching token and user_id.
    Returns a 403 FORBIDDEN status code.
    """
    status_code = HTTPStatus.FORBIDDEN

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaNotAuthorizedError(Exception):
    """
    Exception for when a request is made without a valid user token.
    Returns a 401 UNAUTHORIZED status code.
    """
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaNotFoundError(Exception):
    """
    Exception for when a search for a specific object in either our database or
    the keycloak database is not found. Returns a 404 NOT FOUND status code.
    """
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaBadIdError(Exception):
    """
    Exception for when there is a problem with either keycloak or mongo when trying to get
    user data. Returns a 400 BAD_REQUEST status code.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaBadRequestError(Exception):
    """
    Exception for when there is a problem with either keycloak or mongo when
    trying to post user data. Could either be called when you are missing fields
    or when you have extra fields in your request. Returns a 400 BAD REQUEST status code.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

