from typing import Optional
from datetime import datetime
from pydantic import BaseModel, conlist, constr
from .cleaned_dataset import CleanedDataset


class ModelBase(BaseModel):
    project_id: Optional[int]
    dataset_id: Optional[int]
    name: Optional[constr(min_length=1, strip_whitespace=True)]


# properties to receive on Model creation
class ModelCreate(ModelBase):
    project_id: int
    dataset_id: int
    name: constr(min_length=1, strip_whitespace=True)

    # parameters
    number_of_layers: Optional[conlist(int, min_items=1)]
    maximum_neurons_per_layer: Optional[conlist(int, min_items=1)]
    learning_rate: Optional[conlist(float, min_items=1)]
    batch_size: Optional[conlist(int, min_items=1)]


class ModelInDBBase(ModelBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    is_trained: Optional[bool] = False

    number_of_layers: Optional[int]
    maximum_neurons_per_layer: Optional[int]
    learning_rate: Optional[float]
    batch_size: Optional[int]

    accuracy_score: Optional[float]
    mean_squared_log_error: Optional[float]

    class Config:
        orm_mode = True


# properties to return to the client
class Model(ModelInDBBase):
    ...


class ModelWithDataset(ModelInDBBase):
    dataset: Optional[CleanedDataset]


class ModelParameters(BaseModel):
    number_of_layers: Optional[int]
    middle_layer_size: Optional[int]
    alpha: Optional[float]
    batch_size: Optional[int]