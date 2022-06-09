"""Router for ML Projects."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import projects as project_service
from lighthouse.ml_projects.schemas import ProjectCreate, Project
from lighthouse.ml_projects.exceptions import (
    UnauthenticatedException,
    AppException,
)

router = APIRouter(prefix="/projects")


@router.get('/', responses=UnauthenticatedException.get_example_response())
def get_projects(*,
                 skip: int = 0,
                 limit: int = 100,
                 db: Session = Depends(get_session),
                 user_data=Depends(get_current_user_data)):
    """
    Returns current user projects.
    """
    return project_service.get_user_projects(
        user_id=user_data.user_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=Project)
def create_project(*,
                   project_data: ProjectCreate,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Creates a new project.
    """
    try:
        return project_service.create_project(
            user_id=user_data.user_id,
            project_data=project_data,
            db=db,
        )

    except AppException as e:
        raise e.to_http_exception()
