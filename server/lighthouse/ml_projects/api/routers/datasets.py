"""Router for Datasets."""

from typing import Dict, List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from lighthouse.ml_projects.api import get_session, get_current_user_data
from lighthouse.ml_projects.services import dataset as dataset_service

from lighthouse.ml_projects.exceptions import (
    UnauthenticatedException,
    AppException,
)

from lighthouse.ml_projects.schemas import (
    RawDatasetCreate,
    CleanedDatasetCreate,
    CleanedDatasetWithSources,
    RawDataset,
    CleanedDataset,
)

router = APIRouter(prefix="/datasets")


@router.get('/raw/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[RawDataset])
def get_raw_datasets(*,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_session),
                     user_data=Depends(get_current_user_data)):
    """
    Returns current user raw datasets.
    """
    return dataset_service.get_raw_datasets(
        user_id=user_data.user_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get('/raw/{dataset_id}/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=RawDataset)
def get_raw_dataset(*,
                    dataset_id: int,
                    db: Session = Depends(get_session),
                    user_data=Depends(get_current_user_data)):
    """
    Returns a raw dataset metadata.
    """
    try:
        dataset = dataset_service.get_raw_dataset(
            user_id=user_data.user_id,
            dataset_id=dataset_id,
            db=db,
        )
    except AppException as e:
        raise e.to_http_exception()

    return dataset


@router.post('/raw/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=RawDataset)
def create_raw_dataset(*,
                       raw_dataset_in: RawDatasetCreate,
                       db: Session = Depends(get_session),
                       user_data=Depends(get_current_user_data)):
    """
    Creates a raw dataset.
    """
    try:
        dataset = dataset_service.create_raw_dataset(
            user_id=user_data.user_id,
            raw_dataset_in=raw_dataset_in,
            db=db,
        )
    except AppException as e:
        raise e.to_http_exception()

    return dataset


@router.get('/cleaned/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[CleanedDataset])
def get_cleaned_datasets(*,
                         skip: int = 0,
                         limit: int = 100,
                         db: Session = Depends(get_session),
                         user_data=Depends(get_current_user_data)):
    """
    Returns current user cleaned datasets.
    """
    return dataset_service.get_cleaned_datasets(
        user_id=user_data.user_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get('/cleaned/{dataset_id}/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=CleanedDatasetWithSources)
def get_cleaned_dataset(*,
                        dataset_id: int,
                        db: Session = Depends(get_session),
                        user_data=Depends(get_current_user_data)):
    """
    Returns a processed dataset metadata.
    """
    try:
        dataset = dataset_service.get_cleaned_dataset(
            user_id=user_data.user_id,
            dataset_id=dataset_id,
            db=db,
        )

    except AppException as e:
        raise e.to_http_exception()

    return dataset.dict()


@router.post('/cleaned/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=CleanedDataset)
def create_cleaned_dataset(*,
                           cleaned_dataset_in: CleanedDatasetCreate,
                           db: Session = Depends(get_session),
                           user_data=Depends(get_current_user_data)):
    """
    Creates a processed dataset.
    """
    try:
        dataset = dataset_service.create_cleaned_dataset(
            user_id=user_data.user_id,
            cleaned_dataset_in=cleaned_dataset_in,
            db=db,
        )
    except AppException as e:
        raise e.to_http_exception()

    return dataset
