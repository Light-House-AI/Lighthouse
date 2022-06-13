import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .user import User


class Notification(Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), index=True, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return "Notification(id={}, user_id={}, title={}, body={}, created_at={})".format(
            self.id, self.user_id, self.title, self.body, self.created_at)

    def __str__(self):
        return self.__repr__()
