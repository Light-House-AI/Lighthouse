from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from lighthouse.ml_projects.db import RawDatasetCreationMethod


class RawDatasetBase(BaseModel):
    project_id: Optional[int]
    name: Optional[str]
    creation_method: Optional[RawDatasetCreationMethod]


# properties to receive on RawDataset creation
class RawDatasetCreate(RawDatasetBase):
    name: str
    project_id: int


class RawDatasetInDBBase(RawDatasetBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class RawDataset(RawDatasetInDBBase):
    ...