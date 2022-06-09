"""Router for authenticating users."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import auth as auth_service
from lighthouse.ml_projects.schemas import UserCreate, User, AccessToken, Login
from lighthouse.ml_projects.api import get_session, get_current_user_data

from lighthouse.ml_projects.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthenticatedException,
    AppException,
)

router = APIRouter(prefix="/auth")


@router.get("/me",
            response_model=User,
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
def get_user(db: Session = Depends(get_session),
             user_data=Depends(get_current_user_data)):
    """
    Return the current user.
    """

    try:
        user = auth_service.get_user_by_id(user_id=user_data.user_id, db=db)
    except AppException as e:
        raise e.to_http_exception()

    return user


@router.post("/signup",
             response_model=User,
             status_code=201,
             responses=BadRequestException.get_example_response())
def signup(*, db: Session = Depends(get_session), user_in: UserCreate):
    """
    Create a new user.
    """

    try:
        user = auth_service.signup(user_in=user_in, db=db)
    except AppException as e:
        raise e.to_http_exception()

    return user


@router.post("/login",
             responses=BadRequestException.get_example_response(),
             response_model=AccessToken)
def login(*, db: Session = Depends(get_session), login_data: Login):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    try:
        token = auth_service.login(email=login_data.email,
                                   password=login_data.password,
                                   db=db)
    except AppException as e:
        raise e.to_http_exception()

    return token
