from sqlalchemy import Column, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class Model(Base):
    __table_args__ = (ForeignKeyConstraint(
        columns=['project_id', 'data_id'],
        refcolumns=['data.project_id', 'data.id'],
        name='model_project_id_data_id_fkey'), )

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=func.uuid_generate_v4())

    name = Column(String, nullable=False)

    project_id = Column(UUID(as_uuid=True),
                        ForeignKey(Project.id),
                        primary_key=True)

    data_id = Column(UUID(as_uuid=True), nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="models")
    data = relationship("Data", back_populates="models")

    primary_deployments = relationship(
        "Deployment",
        primaryjoin=
        "and_(Model.project_id==Deployment.project_id, Model.id==Deployment.primary_model_id)",
        back_populates="primary_model",
    )

    secondary_deployments = relationship(
        "Deployment",
        primaryjoin=
        "and_(Model.project_id==Deployment.project_id, Model.id==Deployment.secondary_model_id)",
        back_populates="secondary_model",
    )

    def get_data_cleaning_pipeline_id(self):
        return str(self.project_id) + "-" + str(self.data_id)

    def __repr__(self):
        return "<Model(id={}, name={}, project_id={}, data_id={}, date_created={}, data_cleaning_pipeline_id={})>".format(
            self.id, self.name, self.project_id, self.data_id,
            self.date_created, self.get_data_cleaning_pipeline_id())

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_created": self.date_created,
            "project_id": self.project_id,
            "data_id": self.data_id,
            "data_cleaning_pipeline_id": self.get_data_cleaning_pipeline_id(),
        }