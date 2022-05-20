from sqlalchemy import Column, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class Data(Base):
    # sequences
    version_seq = Sequence('data_version_seq')

    # columns
    version = Column(Integer,
                     version_seq,
                     primary_key=True,
                     server_default=version_seq.next_value())

    project_id = Column(Integer, ForeignKey(Project.id), primary_key=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="data")
    models = relationship("Model", back_populates="data")

    # methods
    def get_data_cleaning_pipeline_id(self):
        return str(self.project_id) + "-" + str(self.version)

    def __repr__(self):
        return "<Data(version={}, project_id={}, date_created]{})>".format(
            self.version, self.project_id, self.date_created)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "version": self.version,
            "project_id": self.project_id,
            "date_created": self.date_created,
        }