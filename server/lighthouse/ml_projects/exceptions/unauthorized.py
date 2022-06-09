from .app_exception import AppException


class UnauthorizedException(AppException):

    status_code = 403
    description = "Unauthorized"

    def __init__(self,
                 message="You don't have permission to perform this action"):

        super().__init__(message)
