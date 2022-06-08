from .app_exception import AppException


class UnauthorizedException(AppException):

    status_code = 403
    message = "You don't have permission to perform this action"
    description = "Unauthorized Error"

    def __init__(self, message=message):
        super().__init__(message)
