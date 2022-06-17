"""Router for checking lighthouse status."""

from fastapi import APIRouter

router = APIRouter()


@router.get('/health', response_model=str)
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return 'OK'
