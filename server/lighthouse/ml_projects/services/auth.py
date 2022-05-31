from typing import Optional, Dict
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from jose import jwt, JWTError

from lighthouse.config import config
from lighthouse.ml_projects.db import User, UserRole
from lighthouse.ml_projects.schemas import UserCreate, TokenData, Token
from lighthouse.ml_projects.services.security import _get_password_hash, _verify_password


def get_user_by_id(*, db: Session, user_id: str) -> User:
    """
    Get a user by its id.
    
    :return: The user.
    :raises Exception: If the user is not found.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception("User not found")

    return user


def login(*, email: str, password: str, db: Session):
    """
    Authenticate a user and return its access token.
    
    :return: The access token.
    :raises Exception: If the user is not found or the password is incorrect.
    """

    user = _authenticate(email=email, password=password, db=db)

    if not user:
        raise Exception("Invalid username or password")

    token_data = TokenData(user_id=str(user.id), role=user.role.value)
    token = Token(access_token=_create_access_token(token_data=token_data),
                  token_type="bearer")

    return token


def signup(*, db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    :return: The created user.
    :raises Exception: If the user already exists.
    :raises Exception: If the the role is admin.
    """

    # check if user already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise Exception("User already exists")

    # check for user role
    user_data = user_in.dict()

    if user_data.get("role") is UserRole.admin:
        raise Exception("Admin user creation is not allowed")

    # hash password
    user_data.pop("password")
    user = User(**user_data)
    user.hashed_password = _get_password_hash(user_in.password)

    # add the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_current_user_data(token: str):
    """
    Get the current user id from the JWT token.
    
    :param token: The JWT token to decode.
    :return: The token data.
    :raises JWTError: If the token is invalid.
    """

    try:
        token_data = _decode_access_token(token=token)

    except JWTError as e:
        raise e

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

    if not _verify_password(password, user.hashed_password):
        return None

    return user


def _decode_access_token(token: str):
    payload = jwt.decode(
        token,
        config.ACCESS_TOKEN_SECRET_KEY,
        algorithms=[config.ACCESS_TOKEN_ALGORITHM],
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
