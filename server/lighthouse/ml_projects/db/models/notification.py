import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .user import User


class Notification(Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), index=True, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return "Notification(id={}, user_id={}, description={}, created_at={})".format(
            self.id, self.user_id, self.description, self.created_at)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "created_at": self.created_at,
        }
