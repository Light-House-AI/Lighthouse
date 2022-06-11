"""Router for Users."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import user as user_service
from lighthouse.ml_projects.schemas import UserCreate, User

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

router = APIRouter(prefix="/users")


@router.get("/me/",
            response_model=User,
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
@catch_app_exceptions
def get_user(db: Session = Depends(get_session),
             user_data=Depends(get_current_user_data)):
    """
    Return the current user.
    """
    return user_service.get_user_by_id(user_id=user_data.user_id, db=db)


@router.post("/signup/",
             response_model=User,
             status_code=201,
             responses=BadRequestException.get_example_response())
@catch_app_exceptions
def signup(*, db: Session = Depends(get_session), user_in: UserCreate):
    """
    Create a new user.
    """
    return user_service.signup(user_in=user_in, db=db)
