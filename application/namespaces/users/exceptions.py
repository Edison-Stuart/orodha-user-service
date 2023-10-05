"""
Contains OrodhaErrors which are thrown by the user routes.
"""
from http import HTTPStatus

class OrodhaNotFoundError(Exception):
    """
    Exception for when a search for a specific object in either our database or
    the keycloak database is not found.
    """
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaBadIdError(Exception):
    """
    Exception for when there is a problem with either keycloak or mongo when trying to get
    user data. Typically is called when there is a BAD_REQUEST error with a 400 code.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaBadRequestError(Exception):
    """
    Exception for when there is a problem with either keycloak or mongo when
    trying to post user data. Could either be called when you are missing fields
    or when you have extra fields in your request.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

