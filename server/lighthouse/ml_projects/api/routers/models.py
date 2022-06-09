"""Router for ML Projects."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import model as model_service
from lighthouse.ml_projects.schemas import ModelCreate, Model
from lighthouse.ml_projects.exceptions import (
    UnauthenticatedException,
    AppException,
)

router = APIRouter(prefix="/models")


@router.get('/', responses=UnauthenticatedException.get_example_response())
def get_models(*,
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_session),
               user_data=Depends(get_current_user_data)):
    """
    Returns current user models.
    """
    return model_service.get_user_models(
        user_id=user_data.user_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=Model)
def create_model(*,
                 model_data: ModelCreate,
                 db: Session = Depends(get_session),
                 user_data=Depends(get_current_user_data)):
    """
    Creates a new model.
    """
    try:
        return model_service.create_model(
            user_id=user_data.user_id,
            model_data=model_data,
            db=db,
        )

    except AppException as e:
        raise e.to_http_exception()
