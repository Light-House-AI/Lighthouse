"""Dataset service"""

from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session, joinedload

from lighthouse.ml_projects.schemas import RawDatasetCreate, CleanedDatasetCreate
from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.services import dataset_file as dataset_file_service
from lighthouse.automl.data_cleaning import service as data_cleaning_service

from lighthouse.ml_projects.mongo import DatasetCleaningRules, ProjectDataColumns

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


def upload_raw_dataset(user_id: str, dataset_id: int, file: UploadFile,
                       db: Session):
    """
    Uploads raw dataset.
    """
    # Check if a record exists
    raw_dataset = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id == dataset_id).first()

    if not raw_dataset:
        raise NotFoundException("Dataset not found.")

    # Save uploaded file
    dataset_path = dataset_file_service.save_raw_dataset_to_local_disk(
        dataset_id=dataset_id, file=file.file)

    # Upload dataset
    dataset_file_service.upload_raw_dataset(dataset_id)

    # Get dataset schema
    dataset_columns = data_cleaning_service.get_dataset_columns(dataset_path)
    ProjectDataColumns(
        project_id=raw_dataset.project_id,
        columns=dataset_columns,
    ).save()

    return {"message": "Dataset uploaded"}


def get_raw_dataset_rows(user_id: str, dataset_id: int, skip: int, limit: int,
                         db: Session):
    """
    Returns raw dataset rows.
    """
    dataset = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id == dataset_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    # Download dataset
    file_path = dataset_file_service.download_raw_dataset(dataset_id)
    rows = data_cleaning_service.get_rows(file_path, skip, limit)

    return rows


def get_raw_dataset_cleaning_rules_recommendations(user_id: str,
                                                   datasets_ids: List[int],
                                                   db: Session):
    """
    Returns raw dataset cleaning rules recommendations.
    """
    datasets = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id.in_(datasets_ids)).all()

    if not len(datasets):
        raise NotFoundException("Datasets not found.")

    # Download datasets
    datasets_paths = [
        dataset_file_service.download_raw_dataset(dataset.id)
        for dataset in datasets
    ]

    predicted_column = datasets[0].project.predicted_column

    rules = data_cleaning_service.get_data_cleaning_suggestions(
        datasets_paths, predicted_column)

    return rules


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
    dataset = db.query(CleanedDataset).options(
        joinedload(CleanedDataset.sources)).join(Project).filter(
            CleanedDataset.id == dataset_id,
            Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    return dataset.to_dict()


def create_cleaned_dataset(user_id: str,
                           cleaned_dataset_in: CleanedDatasetCreate,
                           db: Session):
    """
    Creates a cleaned dataset.
    """
    # Check if project exists
    project = db.query(Project).filter(
        Project.user_id == user_id,
        Project.id == cleaned_dataset_in.project_id).first()

    if not project:
        raise NotFoundException("Project not found.")

    # Get data
    cleaned_dataset_metadata = cleaned_dataset_in.dict()
    rules = cleaned_dataset_metadata.pop("rules")
    raw_datasets_ids = cleaned_dataset_metadata.pop('sources')

    # Create cleaned dataset record
    cleaned_dataset = CleanedDataset(**cleaned_dataset_metadata)
    db.add(cleaned_dataset)

    # Create sources records
    raw_datasets = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id.in_(raw_datasets_ids)).all()

    if not len(raw_datasets):
        raise NotFoundException("Datasets not found.")

    sources = [
        CleanedDatasetSource(raw_dataset=raw_dataset,
                             cleaned_dataset=cleaned_dataset)
        for raw_dataset in raw_datasets
    ]

    db.add_all(sources)
    db.commit()

    # Download datasets
    raw_datasets_file_paths = [
        dataset_file_service.download_raw_dataset(dataset.id)
        for dataset in raw_datasets
    ]

    # Clean datasets
    cleaned_dataset_file_path = dataset_file_service.get_cleaned_dataset_local_path(
        cleaned_dataset.id)

    data_cleaning_service.create_cleaned_dataset(
        raw_datasets_file_paths=raw_datasets_file_paths,
        cleaned_dataset_file_path=cleaned_dataset_file_path,
        rules=rules,
        predicted_column=project.predicted_column)

    # Upload cleaned data
    dataset_file_service.upload_cleaned_dataset(cleaned_dataset.id)

    # Save cleaning rules
    cleaning_rules = DatasetCleaningRules(
        dataset_id=cleaned_dataset.id,
        rules=rules,
    )
    cleaning_rules.save()

    return cleaned_dataset


def get_cleaned_dataset_rows(user_id: str, dataset_id: int, skip: int,
                             limit: int, db: Session):
    """
    Returns cleaned dataset rows.
    """
    dataset = db.query(CleanedDataset).join(Project).filter(
        CleanedDataset.id == dataset_id, Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    # Download dataset
    file_path = dataset_file_service.download_cleaned_dataset(dataset_id)
    rows = data_cleaning_service.get_rows(file_path, skip, limit)

    return rows


def get_cleaned_dataset_cleaning_rules(user_id: int, dataset_id: int,
                                       db: Session):
    """
    Returns the cleaning rules for a cleaned dataset.
    """
    dataset = db.query(CleanedDataset).join(Project).filter(
        CleanedDataset.id == dataset_id, Project.user_id == user_id).count()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    cleaning_rules = DatasetCleaningRules.objects(
        dataset_id=dataset_id).first()

    if not cleaning_rules:
        raise NotFoundException("Cleaning rules not found.")

    return cleaning_rules.to_json()