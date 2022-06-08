from .app_exception import AppException


class BadRequestException(AppException):

    status_code = 400
    message = "Bad Request"
    description = "Bad Request"

    def __init__(self, message=message):
        super().__init__(message)
