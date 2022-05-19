from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Project(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    # relationships
    user = relationship("User", back_populates="projects")
    models = relationship("Model", back_populates="project")
    data = relationship("Data", back_populates="project")
    deployments = relationship("Deployment", back_populates="project")

    def __repr__(self):
        return "<Project(id={}, name={}, user_id={})>".format(
            self.id, self.name, self.user_id)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }