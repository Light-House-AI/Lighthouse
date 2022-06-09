from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .cleaned_dataset import CleanedDataset
from .project import Project


class Model(Base):
    id = Column(Integer, primary_key=True)

    project_id = Column(ForeignKey(Project.id), nullable=False)
    dataset_id = Column(ForeignKey(CleanedDataset.id), nullable=False)

    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="models")
    dataset = relationship("CleanedDataset", back_populates="models")

    primary_deployments = relationship(
        "Deployment",
        primaryjoin="Model.id==Deployment.primary_model_id",
        back_populates="primary_model",
    )

    secondary_deployments = relationship(
        "Deployment",
        primaryjoin="Model.id==Deployment.secondary_model_id",
        back_populates="secondary_model",
    )

    # methods
    def get_data_cleaning_pipeline_id(self):
        return str(self.dataset_id)

    def __repr__(self):
        return "<Model(id={}, project_id={}, dataset_id={}, name={}, created_at={}, data_cleaning_pipeline_id={})>".format(
            self.id, self.name, self.project_id, self.dataset_id,
            self.created_at, self.get_data_cleaning_pipeline_id())

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "dataset_id": self.dataset_id,
            "name": self.name,
            "created_at": self.created_at,
            "data_cleaning_pipeline_id": self.get_data_cleaning_pipeline_id(),
        }
