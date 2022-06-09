from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class CleanedDataset(Base):

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey(Project.id), nullable=False)

    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="cleaned_datasets")
    models = relationship("Model", back_populates="dataset")
    sources = relationship("CleanedDatasetSource")

    # methods
    def get_data_cleaning_pipeline_id(self):
        return str(self.id)

    def __repr__(self):
        return "<CleanedDataset(id={}, project_id={}, name={}, created_at{}, data_cleaning_pipeline_id={})>".format(
            self.id, self.project_id, self.name, self.created_at,
            self.get_data_cleaning_pipeline_id())

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "created_at": self.created_at,
        }
