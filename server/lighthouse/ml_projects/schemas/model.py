from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ModelBase(BaseModel):
    project_id: Optional[int]
    dataset_id: Optional[int]
    name: Optional[str]
    is_trained: Optional[bool] = False

    number_of_layers: Optional[int]
    maximum_neurons_per_layer: Optional[int]
    learning_rate: Optional[float]
    batch_size: Optional[int]


# properties to receive on Model creation
class ModelCreate(ModelBase):
    project_id: int
    dataset_id: int
    name: str

    # parameters
    number_of_layers: Optional[List[int]]
    maximum_neurons_per_layer: Optional[List[int]]
    learning_rate: Optional[List[float]]
    batch_size: Optional[List[int]]


class ModelInDBBase(ModelBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# properties to return to the client
class Model(ModelInDBBase):
    ...


class ModelParameters(BaseModel):
    number_of_layers: Optional[int]
    middle_layer_size: Optional[int]
    alpha: Optional[float]
    batch_size: Optional[int]