import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class UserRole(enum.Enum):
    admin = 'admin'
    user = 'user'


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    projects = relationship("Project", back_populates="user")
