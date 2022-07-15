"""Cleaned Dataset service"""

from typing import List
from sqlalchemy.orm import Session, joinedload

from lighthouse.ml_projects.schemas import CleanedDatasetCreate
from lighthouse.ml_projects.exceptions import NotFoundException

from lighthouse.ml_projects.services import dataset_file as dataset_file_service
from lighthouse.automl.data_cleaning import service as data_cleaning_service
from lighthouse.automl.feature_engineering import FeatureEngineering
from lighthouse.mlops.monitoring import service as monitoring_service

from lighthouse.ml_projects.mongo import (
    DatasetCleaningRules,
    DatasetFeatureRules,
)

from lighthouse.ml_projects.db import (
    CleanedDataset,
    RawDataset,
    Project,
    CleanedDatasetSource,
)


def get_cleaned_datasets(user_id: int,
                         project_id: int,
                         db: Session,
                         skip: int = 0,
                         limit: int = 100):
    """
    Returns user cleaned datasets.
    """
    return db.query(CleanedDataset).join(Project).filter(
        Project.id == project_id,
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


def create_cleaned_dataset(user_id: int,
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

    # Create cleaned dataset record
    cleaned_dataset, raw_datasets = _create_cleaned_dataset_records(
        cleaned_dataset_in,
        db,
    )

    # Download and merge datasets
    (
        merged_df,
        merged_dataset_filename,
        merged_dataset_filepath,
    ) = _download_and_merge_datasets(raw_datasets)

    # Clean dataset
    cleaning_rules = cleaned_dataset_in.dict().pop("rules")
    cleaned_df, cleaned_dataset_file_path = _clean_dataset(
        cleaned_dataset.id,
        cleaning_rules,
        merged_df,
        project.predicted_column,
    )

    # Apply feature engineering
    features_df = _apply_feature_engineering(
        cleaned_dataset.id,
        cleaned_df,
        cleaning_rules,
        project.predicted_column,
        project.type,
    )

    # Upload cleaned data
    _save_and_upload_features_dataset(
        cleaned_dataset.id,
        cleaned_dataset_file_path,
        features_df,
    )

    # Save dataset expectations suite
    monitoring_service.save_dataset_expectations_suite(
        cleaned_dataset.id,
        merged_dataset_filename,
    )

    dataset_file_service.delete_file(merged_dataset_filepath)

    return cleaned_dataset


def _create_cleaned_dataset_records(cleaned_dataset_in: CleanedDatasetCreate,
                                    db: Session):
    """
    Creates cleaned dataset database record.
    """
    cleaned_dataset_metadata = cleaned_dataset_in.dict()
    raw_datasets_ids = cleaned_dataset_metadata.pop('sources')
    cleaned_dataset_metadata.pop("rules")

    # Create cleaned dataset record
    cleaned_dataset = CleanedDataset(**cleaned_dataset_metadata)
    db.add(cleaned_dataset)

    # Create sources records
    raw_datasets = db.query(RawDataset).join(Project).filter(
        Project.id == cleaned_dataset_in.project_id,
        RawDataset.id.in_(raw_datasets_ids)).all()

    if not len(raw_datasets):
        raise NotFoundException("Datasets not found.")

    sources = [
        CleanedDatasetSource(raw_dataset=raw_dataset,
                             cleaned_dataset=cleaned_dataset)
        for raw_dataset in raw_datasets
    ]

    db.add_all(sources)
    db.commit()

    return cleaned_dataset, raw_datasets


def _download_and_merge_datasets(raw_datasets: List[RawDataset]):
    """
    Downloads and merges datasets.
    """
    raw_datasets_file_paths = [
        dataset_file_service.download_raw_dataset(dataset.id)
        for dataset in raw_datasets
    ]

    merged_dataset_filepath, merged_dataset_filename = dataset_file_service.get_temporary_dataset_local_path(
    )

    merged_dataset_df = data_cleaning_service.create_save_merged_dataframe(
        raw_datasets_file_paths, merged_dataset_filepath)

    return merged_dataset_df, merged_dataset_filename, merged_dataset_filepath


def _clean_dataset(cleaned_dataset_id, cleaning_rules, dataframe,
                   predicted_column):
    """
    Clean dataset.
    """
    cleaned_dataset_file_path = dataset_file_service.get_cleaned_dataset_local_path(
        cleaned_dataset_id)

    cleaned_df = data_cleaning_service.clean_train(
        df=dataframe,
        output_column=predicted_column,
        operations=cleaning_rules,
    )

    # Save cleaning rules
    DatasetCleaningRules(
        dataset_id=cleaned_dataset_id,
        rules=cleaning_rules,
    ).save()

    return cleaned_df, cleaned_dataset_file_path


def _apply_feature_engineering(cleaned_dataset_id, cleaned_df, cleaning_rules,
                               predicted_column, project_type):
    """
    Apply feature engineering.
    """

    feature_engineering_service = FeatureEngineering(
        cleaned_df,
        cleaning_rules,
        predicted_column,
        project_type,
    )

    features_df, features_rules = feature_engineering_service.run()

    # Save feature engineering rules
    DatasetFeatureRules(
        dataset_id=cleaned_dataset_id,
        rules=features_rules,
    ).save()

    return features_df


def _save_and_upload_features_dataset(cleaned_dataset_id,
                                      features_dataset_file_path, features_df):
    """
    Save and upload features dataset.
    """
    data_cleaning_service.save_dataframe(
        features_df,
        features_dataset_file_path,
    )

    dataset_file_service.upload_cleaned_dataset(cleaned_dataset_id)

    return features_dataset_file_path


def get_cleaned_dataset_rows(user_id: int, dataset_id: int, skip: int,
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
