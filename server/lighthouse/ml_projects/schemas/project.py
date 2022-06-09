from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from lighthouse.ml_projects.db import Project, ProjectType


class ProjectBase(BaseModel):
    name: Optional[str]
    predicted_column: Optional[str]
    type: Optional[ProjectType]


# properties to receive on Project creation
class ProjectCreate(ProjectBase):
    name: str
    predicted_column: str
    type: ProjectType


class ProjectInDBBase(ProjectBase):
    id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class Project(ProjectInDBBase):
    ...