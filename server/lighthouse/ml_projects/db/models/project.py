from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Project(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="projects")
    models = relationship("Model", back_populates="project")