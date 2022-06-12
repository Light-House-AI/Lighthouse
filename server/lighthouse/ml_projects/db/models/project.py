import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .user import User


class ProjectType(enum.Enum):
    classification = 'classification'
    regression = 'regression'


class Project(Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), index=True, nullable=False)

    name = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    predicted_column = Column(String, nullable=False)
    type = Column(Enum(ProjectType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User", back_populates="projects")
    models = relationship("Model", back_populates="project")
    raw_datasets = relationship("RawDataset", back_populates="project")
    cleaned_datasets = relationship("CleanedDataset", back_populates="project")
    deployments = relationship("Deployment", back_populates="project")

    def __repr__(self):
        return "<Project(id={}, user_id={}, name={}, predicted_column={}, type={}, created_at={})>".format(
            self.id, self.name, self.predicted_column, self.type, self.user_id,
            self.created_at)

    def __str__(self):
        return self.__repr__()
