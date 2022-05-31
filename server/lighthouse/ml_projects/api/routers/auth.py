"""Router for authenticating users."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import auth as auth_service
from lighthouse.ml_projects.schemas import UserCreate, User, Token, Login
from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.api.responses import (not_authenticated_response,
                                                  bad_request_response,
                                                  not_found_response)

router = APIRouter(prefix="/auth")


@router.get("/me",
            response_model=User,
            responses={
                **not_authenticated_response,
                **not_found_response
            })
def get_user(db: Session = Depends(get_session),
             user_data=Depends(get_current_user_data)):
    """
    Return the current user.
    """

    user = auth_service.get_user_by_id(user_id=user_data.id, db=db)
    return user


@router.post("/signup",
             response_model=User,
             status_code=201,
             responses=bad_request_response)
def signup(*, db: Session = Depends(get_session), user_in: UserCreate):
    """
    Create a new user.
    """

    try:
        user = auth_service.signup(db=db, user_in=user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user


@router.post("/login", responses=bad_request_response, response_model=Token)
def login(*, db: Session = Depends(get_session), login_data: Login):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    try:
        token = auth_service.login(email=login_data.username,
                                   password=login_data.password,
                                   db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return token
