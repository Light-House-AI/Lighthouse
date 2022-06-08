from fastapi import HTTPException
from pydantic import BaseModel


class AppException(Exception):
    """
    This is the base class for all application exceptions.
    It shouldn't be used directly.
    """

    status_code = 500
    message = "Internal error"
    description = "Application Error"

    def __init__(self, message=message):
        super().__init__(message)

    def to_http_exception(self):
        """
        Converts this exception to an FastApi HTTP exception.
        """
        return HTTPException(status_code=self.status_code, detail=self.message)

    @classmethod
    def get_example_response(cls):
        return {
            cls.status_code: {
                "model": cls.HTTPError,
                "description": cls.description
            }
        }

    # schema used to generate the error response
    class HTTPError(BaseModel):
        detail: str

        class Config:
            schema_extra = {
                "example": {
                    "detail": "HTTPError raised."
                },
            }