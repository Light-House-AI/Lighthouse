"""Datasets service"""

from typing import Dict
from sqlalchemy.orm import Session

from lighthouse.ml_projects.schemas import RawDatasetCreate, CleanedDatasetCreate
from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.db import (
    CleanedDataset,
    RawDataset,
    Project,
    CleanedDatasetSource,
)


def get_raw_datasets(user_id: str,
                     db: Session,
                     skip: int = 0,
                     limit: int = 100):
    """
    Returns user raw datasets.
    """
    return db.query(RawDataset).join(Project).filter(
        # RawDataset.project_id == Project.id,
        Project.user_id == user_id).offset(skip).limit(limit).all()


def get_raw_dataset(user_id: int, dataset_id: int, db: Session):
    """
    Returns raw dataset.
    """
    dataset = db.query(RawDataset).join(Project).filter(
        RawDataset.id == dataset_id, Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    return dataset


def create_raw_dataset(user_id: str, raw_dataset_in: RawDatasetCreate,
                       db: Session):
    """
    Creates a raw dataset.
    """
    project_exists = db.query(Project).filter(
        Project.user_id == user_id,
        Project.id == raw_dataset_in.project_id).count()

    if not project_exists:
        raise NotFoundException("Project not found.")

    raw_dataset = RawDataset(**raw_dataset_in.dict())

    db.add(raw_dataset)
    db.commit()
    return raw_dataset


def get_cleaned_datasets(user_id: str,
                         db: Session,
                         skip: int = 0,
                         limit: int = 100):
    """
    Returns user cleaned datasets.
    """
    return db.query(CleanedDataset).join(Project).filter(
        Project.user_id == user_id).offset(skip).limit(limit).all()


def get_cleaned_dataset(user_id: int, dataset_id: int, db: Session):
    """
    Returns cleaned dataset.
    """
    dataset = db.query(CleanedDataset).join(CleanedDatasetSource).join(
        Project).filter(CleanedDataset.id == dataset_id,
                        Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    return dataset


def create_cleaned_dataset(user_id: str,
                           cleaned_dataset_in: CleanedDatasetCreate,
                           db: Session):
    """
    Creates a cleaned dataset.
    """
    # Check if project exists
    project_exists = db.query(Project).filter(
        Project.user_id == user_id,
        Project.id == cleaned_dataset_in.project_id).count()

    if not project_exists:
        raise NotFoundException("Project not found.")

    # Get data
    cleaned_dataset_data = cleaned_dataset_in.dict()
    rules = cleaned_dataset_data.pop("rules")
    raw_datasets_ids = cleaned_dataset_data.pop('sources')

    # Create cleaned dataset
    cleaned_dataset = CleanedDataset(**cleaned_dataset_data)
    db.add(cleaned_dataset)

    # Create sources
    raw_datasets = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id.in_(raw_datasets_ids)).all()

    sources = [
        CleanedDatasetSource(raw_dataset=raw_dataset,
                             cleaned_dataset=cleaned_dataset)
        for raw_dataset in raw_datasets
    ]

    db.add_all(sources)
    db.commit()

    # TODO: create rules

    return cleaned_dataset
