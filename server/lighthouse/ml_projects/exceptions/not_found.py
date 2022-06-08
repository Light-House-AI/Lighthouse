from .app_exception import AppException


class NotFoundException(AppException):

    status_code = 404
    message = "Item not found"
    description = "Item Not Found"

    def __init__(self, message=message):
        super().__init__(message)
