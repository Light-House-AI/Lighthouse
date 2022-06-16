from .app_exception import AppException


class NotFoundException(AppException):

    status_code = 404
    description = "Not Found"

    def __init__(self, message="Item not found"):
        super().__init__(message)
