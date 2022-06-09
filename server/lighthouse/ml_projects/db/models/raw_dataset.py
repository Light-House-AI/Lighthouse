import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class RawDatasetCreationMethod(enum.Enum):
    uploaded = 'uploaded'
    captured = 'captured'


class RawDataset(Base):

    id = Column(Integer, primary_key=True, default=func.uuid_generate_v4())
    project_id = Column(ForeignKey(Project.id), nullable=False)

    name = Column(String, nullable=False)
    creation_method = Column(Enum(RawDatasetCreationMethod),
                             nullable=False,
                             default=RawDatasetCreationMethod.uploaded.value)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="raw_datasets")

    # methods
    def __repr__(self):
        return "<RawDataset(id={}, project_id={}, name={}, creation_method={}, created_at]{})>".format(
            self.id, self.project_id, self.name, self.creation_method,
            self.created_at)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "creation_method": self.creation_method,
            "created_at": self.created_at,
        }
