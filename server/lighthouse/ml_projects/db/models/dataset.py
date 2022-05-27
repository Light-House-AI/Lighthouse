from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class Dataset(Base):

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=func.uuid_generate_v4())

    name = Column(String, nullable=False)

    project_id = Column(UUID(as_uuid=True),
                        ForeignKey(Project.id),
                        primary_key=True)

    date_created = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="datasets")
    models = relationship("Model", back_populates="dataset")

    # methods
    def get_data_cleaning_pipeline_id(self):
        return str(self.project_id) + "-" + str(self.id)

    def __repr__(self):
        return "<Data(id={}, name={}, project_id={}, date_created]{})>".format(
            self.id, self.name, self.project_id, self.date_created)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "date_created": self.date_created,
        }