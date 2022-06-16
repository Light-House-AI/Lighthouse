"""Router for Projects."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import project as project_service
from lighthouse.ml_projects.schemas import ProjectCreate, Project
from lighthouse.ml_projects.exceptions import (
    UnauthenticatedException,
    NotFoundException,
)

from lighthouse.ml_projects.api import (
    get_session,
    get_current_user_data,
    catch_app_exceptions,
)

router = APIRouter(prefix="/projects")


@router.get('',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[Project])
@catch_app_exceptions
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


@router.post('',
             responses=UnauthenticatedException.get_example_response(),
             response_model=Project)
@catch_app_exceptions
def create_project(*,
                   project_data: ProjectCreate,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Creates a new project.
    """
    return project_service.create_project(
        user_id=user_data.user_id,
        project_data=project_data,
        db=db,
    )


@router.get('/{project_id}',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response()
            },
            response_model=Project)
@catch_app_exceptions
def get_project(*,
                project_id: int,
                db: Session = Depends(get_session),
                user_data=Depends(get_current_user_data)):
    """
    Returns project.
    """
    return project_service.get_project(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
    )


@router.get('/{project_id}/columns',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response()
            },
            response_model=List[str])
@catch_app_exceptions
def get_project_columns(*,
                        project_id: int,
                        db: Session = Depends(get_session),
                        user_data=Depends(get_current_user_data)):
    """
    Returns project data columns.
    """
    return project_service.get_project_columns(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
    )