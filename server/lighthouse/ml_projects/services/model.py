"""Model service."""

import dramatiq
from typing import Dict
from sqlalchemy.orm import Session
from dramatiq.brokers.redis import RedisBroker

from lighthouse.config import config
from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.schemas import ModelCreate, ModelParameters

from lighthouse.ml_projects.db import (
    CleanedDataset,
    Model,
    Notification,
    Project,
)

redis_broker = RedisBroker(url=config.DRAMATIQ_REDIS_BROKER_URL)
dramatiq.set_broker(redis_broker)


@dramatiq.actor(
    queue_name=config.MODELS_TRAINING_QUEUE_NAME,
    actor_name=config.MODELS_TRAINING_QUEUE_NAME,
)
def train_model(model_id: str, dataset_id: str, model_params: Dict):
    """A header for the training task."""
    ...


def get_user_models(user_id: int,
                    project_id: int,
                    db: Session,
                    skip: int = 0,
                    limit: int = 100):
    """
    Returns current user models.
    """
    return db.query(Model).join(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id).offset(skip).limit(limit).all()


def get_model(user_id: int, model_id: int, db: Session):
    """
    Returns a model.
    """
    model = db.query(Model).join(Project).filter(
        Model.id == model_id,
        Project.user_id == user_id,
    ).first()

    if not model:
        raise NotFoundException("Model not found")

    return model


def create_model(user_id: int, model_data: ModelCreate, db: Session):
    """
    Creates a model.
    """

    # Check if the project exists
    project_id = model_data.project_id
    project = db.query(Project).filter(Project.id == project_id,
                                       Project.user_id == user_id).first()

    if not project:
        raise NotFoundException("Project not found")

    # Check if the dataset exists
    dataset = db.query(CleanedDataset).filter(
        CleanedDataset.id == model_data.dataset_id,
        CleanedDataset.project_id == project_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found")

    # Get model parameters
    model_create_data = model_data.dict()

    parameters = {
        "type": project.type.value.capitalize(),
        "predicted": project.predicted_column,
    }

    for key in [
            "number_of_layers", "maximum_neurons_per_layer", "learning_rate",
            "batch_size"
    ]:
        if key in model_create_data:
            parameters[key] = model_create_data.pop(key)

    # Create the model record
    model = Model(**model_create_data)
    db.add(model)
    db.commit()
    db.refresh(model)

    # Create the training task
    train_model.send(
        model.id,
        dataset.id,
        parameters,
    )

    return model


def mark_model_as_trained(model_id: int, model_params: ModelParameters,
                          db: Session):
    """
    Marks a model as finished.
    """
    # Check if the model exists
    model = db.query(Model).join(Project).filter(Model.id == model_id).first()

    if not model:
        raise NotFoundException("Model not found")

    # Update model status
    model.is_trained = True
    model.number_of_layers = model_params.number_of_layers
    model.maximum_neurons_per_layer = model_params.middle_layer_size
    model.learning_rate = model_params.alpha
    model.batch_size = model_params.batch_size

    # Create notification
    notification = Notification(
        user_id=model.project.user_id,
        title="Model trained",
        body=f'Model {model.name} with id {model.id} is trained',
    )

    db.add(notification)
    db.commit()

    return model
