from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Model(Base):
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    project = relationship("Project", back_populates="models")
