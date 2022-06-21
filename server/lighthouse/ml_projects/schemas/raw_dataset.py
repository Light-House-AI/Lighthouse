from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr, conset
from lighthouse.ml_projects.db import RawDatasetCreationMethod


class RawDatasetBase(BaseModel):
    project_id: Optional[int]
    name: Optional[constr(min_length=1, strip_whitespace=True)]
    creation_method: Optional[RawDatasetCreationMethod]


# properties to receive on RawDataset creation
class RawDatasetCreate(RawDatasetBase):
    name: constr(min_length=1, strip_whitespace=True)
    project_id: int


class RawDatasetInDBBase(RawDatasetBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class RawDataset(RawDatasetInDBBase):
    ...


class RawDatasetsRecommendations(BaseModel):
    datasets_ids: conset(int, min_items=1)
