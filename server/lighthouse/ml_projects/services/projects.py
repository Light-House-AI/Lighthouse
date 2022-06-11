from typing import Dict
from sqlalchemy.orm import Session

from lighthouse.ml_projects.db import Project
from lighthouse.ml_projects.db import Model
from lighthouse.ml_projects.db import Deployment


def get_user_projects(user_id: str,
                      db: Session,
                      skip: int = 0,
                      limit: int = 100):
    """
    Returns current user projects.
    """
    return db.query(Project).filter(
        Project.user_id == user_id).offset(skip).limit(limit).all()


def create_project(user_id: str, name: str, type: str, db: Session):
    """
    Creates a new project.
    """
    project = Project(user_id=user_id, name=name, type=type)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def upload_dataset(project_id: str, data: bytes, db: Session):
    """
    Uploads a dataset to a project.
    """
    pass


def get_dataset_cleaning_rules_recommendations(project_id: str,
                                               dataset_id: str, db: Session):
    """
    Returns dataset cleaning rules recommendations.
    """
    pass


def create_processed_dataset(project_id: str, raw_dataset_id: str, rules: Dict,
                             db: Session):
    """
    Creates a processed dataset.
    """
    pass


def create_model(project_id: str, dataset_id: str, model_type: str,
                 db: Session):
    """
    Creates a model.
    """
    model = Model(project_id=project_id,
                  dataset_id=dataset_id,
                  model_type=model_type)

    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def create_deployment(project_id: str, model_id: str, db: Session):
    """
    Creates a deployment.
    """
    deployment = Deployment(project_id=project_id, model_id=model_id)
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment
