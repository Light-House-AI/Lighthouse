"""Router for deployment."""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
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
    Returns current user projects.
    """
    print(deployment_id, input_data, user_data)
