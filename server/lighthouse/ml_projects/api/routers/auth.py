"""Router for authenticating users."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import auth as auth_service
from lighthouse.ml_projects.schemas import AccessToken, Login
from lighthouse.ml_projects.exceptions import BadRequestException
from lighthouse.ml_projects.api import (
    get_session,
    catch_app_exceptions,
)

router = APIRouter(prefix="/auth")


@router.post('/login',
             responses=BadRequestException.get_example_response(),
             response_model=AccessToken)
@catch_app_exceptions
def login(*, db: Session = Depends(get_session), login_data: Login):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    return auth_service.login(
        email=login_data.email,
        password=login_data.password,
        db=db,
    )
