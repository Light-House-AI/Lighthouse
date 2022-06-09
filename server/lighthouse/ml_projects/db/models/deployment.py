import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .model import Model
from .project import Project


class DeploymentType(enum.Enum):
    champion_challenger = 'champion_challenger'
    single_model = 'single_model'
    fallback = 'fallback'


class Deployment(Base):

    id = Column(Integer, primary_key=True)

    project_id = Column(ForeignKey(Project.id), nullable=False)
    primary_model_id = Column(ForeignKey(Model.id), nullable=False)
    secondary_model_id = Column(ForeignKey(Model.id), nullable=True)

    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_running = Column(Boolean, nullable=False, default=False)
    deployment_type = Column(Enum(DeploymentType),
                             nullable=False,
                             default=DeploymentType.single_model)

    # relationships
    project = relationship("Project", back_populates="deployments")

    primary_model = relationship("Model",
                                 foreign_keys=[primary_model_id],
                                 back_populates="primary_deployments")

    secondary_model = relationship("Model",
                                   foreign_keys=[secondary_model_id],
                                   back_populates="secondary_deployments")

    # methods
    def __repr__(self):
        return "<Deployment(id={}, project_id={}, primary_model_id={}, secondary_model_id={}, name={}, created_at={}, is_running={}, deployment_type={})>".format(
            self.id, self.project_id, self.primary_model_id,
            self.secondary_model_id, self.name, self.created_at,
            self.is_running, self.deployment_type)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "primary_model_id": self.primary_model_id,
            "secondary_model_id": self.secondary_model_id,
            "name": self.name,
            "created_at": self.created_at,
            "is_running": self.is_running,
            "deployment_type": self.deployment_type.value,
        }
