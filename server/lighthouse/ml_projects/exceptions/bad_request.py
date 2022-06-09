from .app_exception import AppException


class BadRequestException(AppException):

    status_code = 400
    description = "Bad Request"

    def __init__(self, message="Bad Request"):
        super().__init__(message)
