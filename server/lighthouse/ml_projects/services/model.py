"""Models service."""

from sqlalchemy.orm import Session

from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.schemas import ModelCreate
from lighthouse.ml_projects.services.celery import celery_app
from lighthouse.ml_projects.db import (CleanedDataset, Model, Notification,
                                       Project)

MODEL_TRAINING_TASK_NAME = 'train_model'


def get_user_models(user_id: int, db: Session, skip: int = 0,
                    limit: int = 100):
    """
    Returns current user models.
    """
    return db.query(Model).join(Project).filter(
        Project.user_id == user_id).offset(skip).limit(limit).all()


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

    # Create the model record
    model = Model(**model_data.dict())
    db.add(model)
    db.commit()
    db.refresh(model)

    # Create the training task
    celery_app.send_task(
        MODEL_TRAINING_TASK_NAME,
        args=[model.id, dataset.id, project.predicted_column],
    )

    return model


def mark_model_as_trained(model_id: int, db: Session):
    """
    Marks a model as finished.
    """
    # Check if the model exists
    model = db.query(Model).join(Project).filter(Model.id == model_id).first()

    if not model:
        raise NotFoundException("Model not found")

    # Update model status
    model.is_trained = True

    # Create notification
    notification = Notification(
        user_id=model.project.user_id,
        description=f'Model {model.name} with id {model.id} is trained',
    )

    db.add(notification)
    db.commit()

    return model
