import enum

from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class UserRole(enum.Enum):
    admin = 'admin'
    user = 'user'


class User(Base):

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=func.uuid_generate_v4())

    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    role = Column(Enum(UserRole), nullable=False, default=UserRole.user.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects = relationship("Project", back_populates="user")

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