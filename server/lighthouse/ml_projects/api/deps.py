"""
Dependencies for the API.
"""

from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request

from lighthouse.ml_projects.services import auth
from lighthouse.ml_projects.exceptions import AppException
from lighthouse.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.LOGIN_ROUTE)


def get_session(request: Request):
    """
    Create and get database session.
    """
    session: sessionmaker = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        session.close()


def get_current_user_data(token: str = Depends(oauth2_scheme)):
    """
    Returns current user data.
    """

    try:
        token_data = auth.get_current_user_data(token=token)
    except AppException as e:
        raise e.to_http_exception()

    return token_data