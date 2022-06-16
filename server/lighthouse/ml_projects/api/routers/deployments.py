"""Router for Deployments."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import deployment as deployment_service
from lighthouse.ml_projects.schemas import Deployment, DeploymentCreate

from lighthouse.ml_projects.api import (
    get_session,
    get_current_user_data,
    catch_app_exceptions,
)

from lighthouse.ml_projects.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthenticatedException,
)

router = APIRouter(prefix="/deployments")


@router.get('',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[Deployment])
@catch_app_exceptions
def get_deployments(*,
                    project_id: int = Query(...),
                    skip: int = 0,
                    limit: int = 10,
                    db: Session = Depends(get_session),
                    user_data=Depends(get_current_user_data)):
    """
    Returns current user deployments.
    """
    return deployment_service.get_deployments(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('',
             responses=UnauthenticatedException.get_example_response(),
             response_model=Deployment)
@catch_app_exceptions
def create_deployment(*,
                      deployment_create: DeploymentCreate,
                      db: Session = Depends(get_session),
                      user_data=Depends(get_current_user_data)):
    """
    Creates a new deployment.
    """
    return deployment_service.create_deployment(
        user_id=user_data.user_id,
        deployment_data=deployment_create,
        db=db,
    )


@router.get('/{deployment_id}',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            },
            response_model=Deployment)
@catch_app_exceptions
def get_deployment(*,
                   deployment_id: int,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Returns a deployment meta data.
    """
    return deployment_service.get_deployment(
        user_id=user_data.user_id,
        deployment_id=deployment_id,
        db=db,
    )


@router.post('/{deployment_id}/predict',
             responses={
                 **UnauthenticatedException.get_example_response(),
                 **BadRequestException.get_example_response(),
                 **NotFoundException.get_example_response(),
             })
@catch_app_exceptions
def get_prediction(*,
                   deployment_id: int,
                   input_data: dict,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Returns the predictions from the deployed model.
    """
    return deployment_service.get_prediction(
        deployment_id=str(deployment_id),
        user_id=user_data.user_id,
        input_data=input_data,
        db=db,
    )
