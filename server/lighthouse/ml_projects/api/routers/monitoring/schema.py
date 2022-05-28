from pydantic import BaseModel


class HealthCheck(BaseModel):
    """
    HealthCheck schema
    """

    status: str
