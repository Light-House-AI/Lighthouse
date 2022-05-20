import enum
from sqlalchemy import Column, DateTime, String, ForeignKey, Enum, Boolean, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
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
            columns=['project_id', 'primary_model_id'],
            refcolumns=['model.project_id', 'model.id'],
            name='deployment_project_id_primary_model_id_fkey'),
        ForeignKeyConstraint(
            columns=['project_id', 'secondary_model_id'],
            refcolumns=['model.project_id', 'model.id'],
            name='deployment_project_id_secondary_model_id_fkey'),
    )

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=func.uuid_generate_v4())

    name = Column(String, nullable=False)

    project_id = Column(UUID(as_uuid=True),
                        ForeignKey(Project.id),
                        primary_key=True)

    deployment_type = Column(Enum(DeploymentType),
                             nullable=False,
                             default=DeploymentType.single_model)

    ## The model id that is deployed
    primary_model_id = Column(UUID(as_uuid=True), nullable=False)
    secondary_model_id = Column(UUID(as_uuid=True), nullable=True)

    ## deployment metadata
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    is_running = Column(Boolean, nullable=False, default=False)

    # relationships
    project = relationship("Project", back_populates="deployments")

    primary_model = relationship("Model",
                                 foreign_keys=[project_id, primary_model_id],
                                 back_populates="primary_deployments")

    secondary_model = relationship(
        "Model",
        foreign_keys=[project_id, secondary_model_id],
        back_populates="secondary_deployments")

    # methods
    def __repr__(self):
        return "<Deployment(id={}, name={}, project_id={}, deployment_type={}, primary_model_id={}, secondary_model_id={}, date_created={}, is_running={})>".format(
            self.id, self.name, self.project_id, self.deployment_type,
            self.primary_model_id, self.secondary_model_id, self.date_created,
            self.is_running)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "deployment_type": self.deployment_type.value,
            "primary_model_id": self.primary_model_id,
            "secondary_model_id": self.secondary_model_id,
            "date_created": self.date_created,
            "is_running": self.is_running,
        }