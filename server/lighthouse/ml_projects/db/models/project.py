import enum

from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .user import User


class ProjectType(enum.Enum):
    classification = 'classification'
    regression = 'regression'


class Project(Base):

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=func.uuid_generate_v4())

    name = Column(String, nullable=False)
    type = Column(Enum(ProjectType), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

    # relationships
    user = relationship("User", back_populates="projects")
    models = relationship("Model", back_populates="project")
    datasets = relationship("Dataset", back_populates="project")
    deployments = relationship("Deployment", back_populates="project")

    def __repr__(self):
        return "<Project(id={}, name={}, type={}, user_id={})>".format(
            self.id, self.name, self.type, self.user_id)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "user_id": self.user_id,
        }