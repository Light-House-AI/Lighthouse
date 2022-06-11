"""Authentication service"""

from typing import Optional, Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError
from sqlalchemy.orm.session import Session

from lighthouse.config import config
from lighthouse.ml_projects.db import User
from lighthouse.ml_projects.schemas import TokenData, AccessToken

from lighthouse.ml_projects.services.password import verify_password

from lighthouse.ml_projects.exceptions import (
    BadRequestException,
    UnauthenticatedException,
)


def login(*, email: str, password: str, db: Session):
    """
    Authenticate a user and return its access token.
    
    :return: The access token.
    :raises BadRequestException: If the user is not found or the password is incorrect.
    """

    user = _authenticate(email=email, password=password, db=db)

    if not user:
        raise BadRequestException("Invalid username or password")

    token_data = TokenData(user_id=str(user.id), role=user.role.value)
    token = AccessToken(
        access_token=_create_access_token(token_data=token_data),
        token_type="bearer")

    return token


def get_current_user_data(token: str):
    """
    Get the current user id from the JWT token.
    
    :param token: The JWT token to decode.
    :return: The token data.
    :raises UnauthenticatedException: If the token is invalid.
    """

    try:
        token_data = _decode_access_token(token=token)

    except JWTError:
        raise UnauthenticatedException("Invalid token, please login again")

    return token_data


def _authenticate(
        *,
        email: str,
        password: str,
        db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def _decode_access_token(token: str):
    payload = jwt.decode(
        token,
        config.ACCESS_TOKEN_SECRET_KEY,
        algorithms=[config.JWT_ALGORITHM],
        options={"verify_aud": False},
    )

    token_data = TokenData(**payload)
    return token_data


def _create_access_token(token_data: TokenData):
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_data=token_data.dict(),
        algorithm=config.JWT_ALGORITHM,
        token_secret_key=config.ACCESS_TOKEN_SECRET_KEY,
    )


def _create_token(*, token_type: str, token_data: Dict[str, str],
                  lifetime: timedelta, algorithm: str,
                  token_secret_key: str) -> str:
    """
    Creates a JWT token.
    
    :param token_type: The type of token to create.
    :param token_data: The data to encode in the token.
    :param lifetime: The lifetime of the token.
    :param algorithm: The algorithm to use for encryption.
    :param token_secret_key: The secret key to use for the token.
    """

    payload = token_data.copy()

    # Set the token type
    payload["type"] = token_type

    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = datetime.utcnow() + lifetime

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    return jwt.encode(payload, token_secret_key, algorithm=algorithm)
