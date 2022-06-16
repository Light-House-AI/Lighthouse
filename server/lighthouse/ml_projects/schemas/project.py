from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr
from lighthouse.ml_projects.db import ProjectType


class ProjectBase(BaseModel):
    name: Optional[constr(min_length=1, strip_whitespace=True)]
    overview: Optional[constr(min_length=1)]
    predicted_column: Optional[constr(min_length=1)]
    type: Optional[ProjectType]


# properties to receive on Project creation
class ProjectCreate(ProjectBase):
    name: constr(min_length=1, strip_whitespace=True)
    overview: constr(min_length=1)
    predicted_column: constr(min_length=1)
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