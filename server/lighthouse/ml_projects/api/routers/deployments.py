"""Router for deployment."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import deployment as deployment_service

from lighthouse.ml_projects.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthenticatedException,
    AppException,
)

router = APIRouter(prefix="/deployments")


@router.post('/{deployment_id}/predict/',
             responses={
                 **UnauthenticatedException.get_example_response(),
                 **BadRequestException.get_example_response(),
                 **NotFoundException.get_example_response(),
             })
def get_prediction(*,
                   deployment_id: int,
                   input_data: dict,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Returns the predictions from the deployed model.
    """

    try:

        return deployment_service.get_prediction(
            deployment_id=str(deployment_id),
            user_id=user_data.user_id,
            input_data=input_data,
            db=db)

    except AppException as e:
        raise e.to_http_exception()
