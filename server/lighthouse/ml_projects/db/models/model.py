from sqlalchemy import Column, Integer, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class Model(Base):
    __table_args__ = (ForeignKeyConstraint(
        columns=['project_id', 'data_version'],
        refcolumns=['data.project_id', 'data.version'],
        name='model_project_id_data_version_fkey'), )

    version = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id), primary_key=True)
    data_version = Column(Integer, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="models")
    data = relationship("Data", back_populates="models")

    primary_deployments = relationship(
        "Deployment",
        primaryjoin=
        "and_(Model.project_id==Deployment.project_id, Model.version==Deployment.primary_model_version)",
        back_populates="primary_model",
    )

    secondary_deployments = relationship(
        "Deployment",
        primaryjoin=
        "and_(Model.project_id==Deployment.project_id, Model.version==Deployment.secondary_model_version)",
        back_populates="secondary_model",
    )

    def get_data_cleaning_pipeline_id(self):
        return str(self.project_id) + "-" + str(self.version)

    def __repr__(self):
        return "<Model(version={}, project_id={}, data_version={}, date_created={}, data_cleaning_pipeline_id={})>".format(
            self.version, self.project_id, self.data_version,
            self.date_created, self.get_data_cleaning_pipeline_id())

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "version": self.version,
            "date_created": self.date_created,
            "project_id": self.project_id,
            "data_version": self.data_version,
            "data_cleaning_pipeline_id": self.get_data_cleaning_pipeline_id(),
        }