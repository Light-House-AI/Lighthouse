import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class UserRole(enum.Enum):
    admin = 'admin'
    user = 'user'


class User(Base):

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    role = Column(Enum(UserRole), nullable=False, default=UserRole.user.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    projects = relationship("Project", back_populates="user")

    # methods
    def __repr__(self):
        return "<User(id={}, email={}, first_name={}, last_name={}, role={}, created_at={})>".format(
            self.id, self.email, self.first_name, self.last_name, self.role,
            self.created_at)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "created_at": self.created_at,
        }

    def is_admin(self):
        return self.role == UserRole.admin

    def get_hashed_password(self):
        return self.hashed_password
