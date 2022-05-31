"""Router for checking lighthouse status."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthCheck(BaseModel):
    """
    HealthCheck schema
    """

    status: str


@router.get('/health', response_model=HealthCheck)
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return HealthCheck(status='OK')
