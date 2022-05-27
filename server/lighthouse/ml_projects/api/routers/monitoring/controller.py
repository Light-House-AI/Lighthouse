from fastapi import APIRouter
from .schema import HealthCheck

router = APIRouter()


@router.get('/health', response_model=HealthCheck)
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return HealthCheck(status='OK')
