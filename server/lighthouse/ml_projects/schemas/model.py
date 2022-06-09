from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ModelBase(BaseModel):
    project_id: Optional[int]
    dataset_id: Optional[int]
    name: Optional[str]
    is_trained: Optional[bool] = False


# properties to receive on Model creation
class ModelCreate(ModelBase):
    project_id: int
    dataset_id: int
    name: str


class ModelInDBBase(ModelBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class Model(ModelInDBBase):
    ...