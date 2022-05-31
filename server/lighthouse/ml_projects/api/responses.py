from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "HTTPException raised."
            },
        }


not_found_response = {
    404: {
        "model": HTTPError,
        "description": "Item not found"
    }
}

forbidden_response = {
    403: {
        "model": HTTPError,
        "description": "Not enough privileges to perform this action"
    }
}

bad_request_response = {
    400: {
        "model": HTTPError,
        "description": "Bad request"
    }
}

not_authenticated_response = {
    401: {
        "model": HTTPError,
        "description": "Not authenticated, please login."
    }
}