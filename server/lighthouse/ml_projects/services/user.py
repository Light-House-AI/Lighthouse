"""User service."""

from sqlalchemy.orm.session import Session

from lighthouse.ml_projects.db import User, UserRole, Notification
from lighthouse.ml_projects.schemas import UserCreate

from lighthouse.ml_projects.services.password import get_password_hash

from lighthouse.ml_projects.exceptions import (
    NotFoundException,
    BadRequestException,
)


def get_user_by_id(*, user_id: int, db: Session) -> User:
    """
    Get a user by its id.
    
    :return: The user.
    :raises NotFoundException: If the user is not found.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    return user


def signup(*, user_in: UserCreate, db: Session) -> User:
    """
    Create a new user.
    
    :return: The created user.
    :raises BadRequestException: If the user already exists or the the role is admin.
    """

    # check if user already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise BadRequestException("User already exists")

    # check for user role
    user_data = user_in.dict()

    if user_data.get("role") is UserRole.admin:
        raise BadRequestException("Admin user creation is not allowed")

    # hash password
    user_data.pop("password")
    user = User(**user_data)
    user.hashed_password = get_password_hash(user_in.password)

    # add the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_notifications(*, user_id: int, skip: int, limit: int,
                           db: Session) -> list:
    """
    Get the notifications for a user.
    """

    return db.query(Notification).filter(
        Notification.user_id == user_id).offset(skip).limit(limit).all()
