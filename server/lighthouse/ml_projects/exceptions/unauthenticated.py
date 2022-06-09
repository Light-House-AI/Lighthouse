from .app_exception import AppException


class UnauthenticatedException(AppException):

    status_code = 401
    description = "Unauthenticated"

    def __init__(self,
                 message="You don't have permission to perform this action"):

        super().__init__(message)
