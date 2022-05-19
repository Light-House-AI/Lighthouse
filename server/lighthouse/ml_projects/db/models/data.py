from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from .base import Base
from .project import Project


class Data(Base):
    version = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id), primary_key=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    project = relationship("Project", back_populates="data")
    models = relationship("Model", back_populates="data")

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