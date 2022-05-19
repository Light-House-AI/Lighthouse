import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class DeploymentType(enum.Enum):
    champion_challenger = 'champion_challenger'
    single_model = 'single_model'
    fallback = 'fallback'


class Deployment(Base):
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['project_id', 'primary_model_version'],
            refcolumns=['model.project_id', 'model.version'],
            name='deployment_project_id_primary_model_version_fkey'),
        ForeignKeyConstraint(
            columns=['project_id', 'secondary_model_version'],
            refcolumns=['model.project_id', 'model.version'],
            name='deployment_project_id_secondary_model_version_fkey'),
    )

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id), primary_key=True)

    deployment_type = Column(Enum(DeploymentType),
                             nullable=False,
                             default=DeploymentType.single_model)

    # The model version that is deployed
    primary_model_version = Column(Integer, nullable=False)
    secondary_model_version = Column(Integer, nullable=True)

    # deployment metadata
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    is_running = Column(Boolean, nullable=False, default=False)

    # relationships
    project = relationship("Project", back_populates="deployments")

    primary_model = relationship(
        "Model",
        foreign_keys=[project_id, primary_model_version],
        back_populates="primary_deployments")

    secondary_model = relationship(
        "Model",
        foreign_keys=[project_id, secondary_model_version],
        back_populates="secondary_deployments")

    # methods
    def __repr__(self):
        return "<Deployment(id={}, project_id={}, deployment_type={}, primary_model_version={}, secondary_model_version={}, date_created={}, is_running={})>".format(
            self.id, self.project_id, self.deployment_type,
            self.primary_model_version, self.secondary_model_version,
            self.date_created, self.is_running)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "deployment_type": self.deployment_type.value,
            "primary_model_version": self.primary_model_version,
            "secondary_model_version": self.secondary_model_version,
            "date_created": self.date_created,
            "is_running": self.is_running,
        }