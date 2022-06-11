from typing import Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel, conset


class CleanedDatasetSource(BaseModel):
    cleaned_dataset_id: int
    raw_dataset_id: int


class CleanedDatasetBase(BaseModel):
    project_id: Optional[int]
    name: Optional[str]


# properties to receive on CleanedDataset creation
class CleanedDatasetCreate(CleanedDatasetBase):
    name: str
    project_id: int
    sources: conset(int, min_items=1)
    rules: List[Dict]


class CleanedDatasetInDBBase(CleanedDatasetBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class CleanedDataset(CleanedDatasetInDBBase):
    ...


class CleanedDatasetWithSources(CleanedDataset):
    sources: List[CleanedDatasetSource]