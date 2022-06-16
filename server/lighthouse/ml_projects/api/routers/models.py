"""Router for Models."""

from typing import List
from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from lighthouse.config import config
from lighthouse.ml_projects.services import model as model_service
from lighthouse.ml_projects.schemas import ModelCreate, Model, ModelParameters
from lighthouse.ml_projects.exceptions import UnauthenticatedException

from lighthouse.ml_projects.api import (
    get_session,
    get_current_user_data,
    catch_app_exceptions,
)
from lighthouse.ml_projects.exceptions.not_found import NotFoundException

router = APIRouter(prefix="/models")


@router.get('',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[Model])
@catch_app_exceptions
def get_models(*,
               project_id: int = Query(...),
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_session),
               user_data=Depends(get_current_user_data)):
    """
    Returns current user models.
    """
    return model_service.get_user_models(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('',
             responses=UnauthenticatedException.get_example_response(),
             response_model=Model)
@catch_app_exceptions
def create_model(*,
                 model_data: ModelCreate,
                 db: Session = Depends(get_session),
                 user_data=Depends(get_current_user_data)):
    """
    Creates a new model.
    """
    return model_service.create_model(
        user_id=user_data.user_id,
        model_data=model_data,
        db=db,
    )


@router.get('/{model_id}',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response()
            },
            response_model=Model)
@catch_app_exceptions
def get_model(*,
              model_id: str,
              db: Session = Depends(get_session),
              user_data=Depends(get_current_user_data)):
    """ 
    Returns a model.
    """
    return model_service.get_model(
        user_id=user_data.user_id,
        model_id=model_id,
        db=db,
    )


@router.post('/{model_id}/training_status',
             responses={
                 **UnauthenticatedException.get_example_response(),
                 **NotFoundException.get_example_response()
             })
@catch_app_exceptions
def update_model_training_status(*,
                                 model_id: int,
                                 model_params: ModelParameters,
                                 x_token: str = Header(None),
                                 db: Session = Depends(get_session)):
    """
    A webhook to update model training status.
    """
    if x_token != config.WEBHOOK_TOKEN:
        raise UnauthenticatedException("Invalid webhook token.")

    model_service.mark_model_as_trained(
        model_id=model_id,
        db=db,
        model_params=model_params,
    )

    return {"message": "Model status updated."}
