"""Router for deployment."""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import deployments as deployments_service
from lighthouse.ml_projects.api.responses import (not_authenticated_response,
                                                  not_found_response)

router = APIRouter(prefix="/deployments")


@router.post('/{deployment_id}/predict',
             responses={
                 **not_authenticated_response,
                 **not_found_response
             })
def get_prediction(*,
                   deployment_id: UUID,
                   input_data: dict,
                   db: Session = Depends(get_session),
                   user_data=Depends(get_current_user_data)):
    """
    Returns the predictions from the deployed model.
    """
    return deployments_service.get_prediction(deployment_id=str(deployment_id),
                                              user_id=user_data.user_id,
                                              input_data=input_data,
                                              db=db)
