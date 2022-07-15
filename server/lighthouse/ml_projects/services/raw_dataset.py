"""Raw Dataset service"""

from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session

from lighthouse.ml_projects.schemas import RawDatasetCreate
from lighthouse.ml_projects.mongo import ProjectDataColumns
from lighthouse.ml_projects.exceptions import NotFoundException, BadRequestException

from lighthouse.ml_projects.services import dataset_file as dataset_file_service
from lighthouse.automl.data_cleaning import service as data_cleaning_service
from lighthouse.automl.data_cleaning import visualization as data_visualization_service
from lighthouse.mlops.monitoring import service as monitoring_service

from lighthouse.ml_projects.db import (
    RawDataset,
    RawDatasetCreationMethod,
    Project,
)


def get_raw_datasets(user_id: int,
                     project_id: int,
                     db: Session,
                     skip: int = 0,
                     limit: int = 100):
    """
    Returns user raw datasets.
    """
    return db.query(RawDataset).join(Project).filter(
        Project.id == project_id,
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


def create_raw_dataset(user_id: int, raw_dataset_in: RawDatasetCreate,
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


def upload_raw_dataset(user_id: int, dataset_id: int, file: UploadFile,
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

    # Save dataset schema
    _save_dataset_schema(dataset_path, raw_dataset.project_id)

    return {"message": "Dataset uploaded"}


def _save_dataset_schema(dataset_path: str, project_id: int):
    """
    Saves dataset schema.
    """
    dataset_columns = data_cleaning_service.get_dataset_columns(dataset_path)

    ProjectDataColumns(
        project_id=project_id,
        columns=dataset_columns,
    ).save()


def get_raw_dataset_rows(user_id: int, dataset_id: int, skip: int, limit: int,
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


def get_raw_dataset_cleaning_rules_recommendations(user_id: int,
                                                   datasets_ids: List[int],
                                                   db: Session):
    """
    Returns raw dataset cleaning rules recommendations.
    """
    datasets = db.query(RawDataset).join(Project).filter(
        Project.user_id == user_id, RawDataset.id.in_(datasets_ids)).all()

    if not len(datasets):
        raise NotFoundException("Datasets not found.")

    dataframe, predicted_column = _get_merged_dataframe_and_predicted_column(
        datasets)

    rules = data_cleaning_service.get_data_cleaning_suggestions(
        dataframe,
        predicted_column,
    )

    statistics = data_cleaning_service.get_dataset_statistics(
        dataframe,
        predicted_column,
    )

    return '{"rules": ' + rules + ', "statistics": ' + statistics + '}'


def _get_merged_dataframe_and_predicted_column(datasets: List[RawDataset]):
    """
    Downloads datasets and returns merged dataframe.
    """
    datasets_paths = [
        dataset_file_service.download_raw_dataset(dataset.id)
        for dataset in datasets
    ]

    dataframe = data_cleaning_service.create_merged_data_frame(datasets_paths)
    predicted_column = datasets[0].project.predicted_column

    return dataframe, predicted_column


def create_raw_dataset_from_project_shadow_data(
        user_id: int, raw_dataset_in: RawDatasetCreate, db: Session) -> None:
    """
    Create dataset from shadow data.
    """

    project = db.query(Project).filter(
        Project.id == raw_dataset_in.project_id,
        Project.user_id == user_id,
    ).first()

    if not project:
        raise NotFoundException("Project not found.")

    # Get data
    shadow_data = monitoring_service.get_project_labeled_shadow_data(
        project_id=project.id,
        predicted_column_name=project.predicted_column,
    )

    # Check if there is data
    if len(shadow_data) == 0:
        raise BadRequestException("No labeled input data found.")

    return _create_raw_dataset_from_shadow_data(
        raw_dataset_in=raw_dataset_in,
        shadow_data=shadow_data,
        db=db,
    )


def _create_raw_dataset_from_shadow_data(raw_dataset_in: RawDatasetCreate,
                                         shadow_data: List[dict],
                                         db: Session) -> RawDataset:
    # Create dataset record
    raw_dataset_in.creation_method = RawDatasetCreationMethod.capture
    dataset = RawDataset(**raw_dataset_in.dict())
    db.add(dataset)
    db.commit()

    # Save & upload dataset
    dataset_file_service.save_dicts_as_raw_dataset_file(
        dataset.id,
        shadow_data,
    )
    dataset_file_service.upload_raw_dataset(dataset.id)

    return dataset


def get_raw_dataset_correlation(user_id: int, dataset_id: int, db: Session):
    """
    Returns the correlation between the columns of a raw dataset.
    """
    dataset = db.query(RawDataset).join(Project).filter(
        RawDataset.id == dataset_id, Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    # Download dataset
    file_path = dataset_file_service.download_raw_dataset(dataset_id)
    df = data_cleaning_service.get_dataframe(file_path)

    return data_visualization_service.get_correlation(df)


def get_raw_dataset_visualization(user_id: int, dataset_id: int,
                                  columns: List[str], db: Session):
    """
    Returns the visualization of a raw dataset.
    """
    dataset = db.query(RawDataset).join(Project).filter(
        RawDataset.id == dataset_id, Project.user_id == user_id).first()

    if not dataset:
        raise NotFoundException("Dataset not found.")

    # Download dataset
    file_path = dataset_file_service.download_raw_dataset(dataset_id)
    df = data_cleaning_service.get_dataframe(file_path)

    return data_visualization_service.get_columns_visualization(df, columns)