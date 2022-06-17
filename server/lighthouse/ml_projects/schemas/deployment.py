from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, constr
from lighthouse.ml_projects.db import DeploymentType


class DeploymentBase(BaseModel):
    project_id: Optional[int]
    primary_model_id: Optional[int]
    secondary_model_id: Optional[int]

    name: Optional[constr(min_length=1, strip_whitespace=True)]
    is_running: Optional[bool]
    type: Optional[DeploymentType]

    @validator('type')
    def type_with_deployments_ids(cls, type, values):
        if type == DeploymentType.champion_challenger and not values[
                'secondary_model_id']:
            raise ValueError(
                "secondary_model_id is required for champion challenger deployment."
            )

        if type == DeploymentType.single_model and values['secondary_model_id']:
            raise ValueError(
                " secondary_model_id is not required for single model deployment."
            )

        return type


# properties to receive on Deployment creation
class DeploymentCreate(DeploymentBase):
    project_id: int
    primary_model_id: int
    name: constr(min_length=1, strip_whitespace=True)
    type: DeploymentType


class DeploymentInDBBase(DeploymentBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class Deployment(DeploymentInDBBase):
    ...