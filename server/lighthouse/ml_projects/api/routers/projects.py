"""Router for ML Projects."""

from http.client import responses
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import projects as projects_service
from lighthouse.ml_projects.api.responses import not_authenticated_response

router = APIRouter(prefix="/projects")


@router.get('/', responses=not_authenticated_response)
def get_projects(*,
                 skip: int = 0,
                 limit: int = 100,
                 db: Session = Depends(get_session),
                 user_data=Depends(get_current_user_data)):
    """
    Returns current user projects.
    """
    return projects_service.get_user_projects(user_id=user_data.id,
                                              db=db,
                                              skip=skip,
                                              limit=limit)
