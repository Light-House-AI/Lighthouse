from .app_exception import AppException


class UnauthenticatedException(AppException):

    status_code = 401
    message = "You don't have permission to perform this action"
    description = "Unauthenticated Error"

    def __init__(self, message=message):
        super().__init__(message)
