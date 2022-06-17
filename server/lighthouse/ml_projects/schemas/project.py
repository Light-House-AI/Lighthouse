from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, constr

from lighthouse.ml_projects.db import ProjectType
from lighthouse.ml_projects.schemas import (
    Deployment,
    Model,
    RawDataset,
    CleanedDataset,
)


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
    num_models: int
    num_deployments: int
    num_raw_datasets: int
    num_cleaned_datasets: int


class ProjectWithRelationships(ProjectInDBBase):
    models: List[Model]
    raw_datasets: List[RawDataset]
    cleaned_datasets: List[CleanedDataset]
    deployments: List[Deployment]
