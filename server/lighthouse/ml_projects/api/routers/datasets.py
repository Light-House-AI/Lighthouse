"""Router for Datasets."""

from typing import List, Dict
from fastapi import APIRouter, Depends, UploadFile, Response
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import dataset as dataset_service
from lighthouse.ml_projects.exceptions import (
    UnauthenticatedException,
    NotFoundException,
)

from lighthouse.ml_projects.api import (
    get_session,
    get_current_user_data,
    catch_app_exceptions,
)

from lighthouse.ml_projects.schemas import (
    RawDatasetCreate,
    CleanedDatasetCreate,
    CleanedDatasetWithSources,
    RawDataset,
    CleanedDataset,
    DatasetCleaningRules,
    RawDatasetsRecommendations,
)

router = APIRouter(prefix="/datasets")


@router.get('/raw/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[RawDataset])
@catch_app_exceptions
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


@router.get('/raw/recommendations/',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            },
            response_model=List[Dict])
@catch_app_exceptions
def get_raw_dataset_cleaning_rules_recommendations(
        *,
        data_in: RawDatasetsRecommendations,
        db: Session = Depends(get_session),
        user_data=Depends(get_current_user_data)):
    """
    Returns raw dataset cleaning rules recommendations.
    """
    return dataset_service.get_raw_dataset_cleaning_rules_recommendations(
        user_id=user_data.user_id,
        datasets_ids=data_in.datasets_ids,
        db=db,
    )


@router.get('/raw/{dataset_id}/',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            },
            response_model=RawDataset)
@catch_app_exceptions
def get_raw_dataset(*,
                    dataset_id: int,
                    db: Session = Depends(get_session),
                    user_data=Depends(get_current_user_data)):
    """
    Returns a raw dataset metadata.
    """
    return dataset_service.get_raw_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )


@router.post('/raw/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=RawDataset)
@catch_app_exceptions
def create_raw_dataset(*,
                       raw_dataset_in: RawDatasetCreate,
                       db: Session = Depends(get_session),
                       user_data=Depends(get_current_user_data)):
    """
    Creates a raw dataset.
    """
    return dataset_service.create_raw_dataset(
        user_id=user_data.user_id,
        raw_dataset_in=raw_dataset_in,
        db=db,
    )


@router.post('/raw/{dataset_id}/upload/',
             responses={
                 **UnauthenticatedException.get_example_response(),
                 **NotFoundException.get_example_response(),
             })
@catch_app_exceptions
def upload_raw_dataset(*,
                       dataset_id: int,
                       file: UploadFile,
                       db: Session = Depends(get_session),
                       user_data=Depends(get_current_user_data)):
    """
    Uploads a raw dataset.
    """
    return dataset_service.upload_raw_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        file=file,
        db=db,
    )


@router.get('/raw/{dataset_id}/rows/',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
@catch_app_exceptions
def get_raw_dataset_rows(*,
                         dataset_id: int,
                         skip: int = 0,
                         limit: int = 100,
                         db: Session = Depends(get_session),
                         user_data=Depends(get_current_user_data)):
    """
    Returns raw dataset rows.
    """
    rows = dataset_service.get_raw_dataset_rows(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        skip=skip,
        limit=limit,
        db=db,
    )

    return Response(rows, media_type="application/json")


@router.get('/cleaned/',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[CleanedDataset])
@catch_app_exceptions
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
@catch_app_exceptions
def get_cleaned_dataset(*,
                        dataset_id: int,
                        db: Session = Depends(get_session),
                        user_data=Depends(get_current_user_data)):
    """
    Returns a processed dataset metadata.
    """
    return dataset_service.get_cleaned_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )


@router.post('/cleaned/',
             responses=UnauthenticatedException.get_example_response(),
             response_model=CleanedDataset)
@catch_app_exceptions
def create_cleaned_dataset(*,
                           cleaned_dataset_in: CleanedDatasetCreate,
                           db: Session = Depends(get_session),
                           user_data=Depends(get_current_user_data)):
    """
    Creates a processed dataset.
    """
    return dataset_service.create_cleaned_dataset(
        user_id=user_data.user_id,
        cleaned_dataset_in=cleaned_dataset_in,
        db=db,
    )


@router.get('/cleaned/{dataset_id}/rows/',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
@catch_app_exceptions
def get_cleaned_dataset_rows(*,
                             dataset_id: int,
                             skip: int = 0,
                             limit: int = 100,
                             db: Session = Depends(get_session),
                             user_data=Depends(get_current_user_data)):
    """
    Returns cleaned dataset rows.
    """
    rows = dataset_service.get_cleaned_dataset_rows(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        skip=skip,
        limit=limit,
        db=db,
    )

    return Response(rows, media_type="application/json")


@router.get('/cleaned/{dataset_id}/cleaning_rules',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            },
            response_model=DatasetCleaningRules)
@catch_app_exceptions
def get_cleaned_dataset_cleaning_rules(
        *,
        dataset_id: int,
        db: Session = Depends(get_session),
        user_data=Depends(get_current_user_data)):
    """
    Returns the cleaning rules for a cleaned dataset.
    """
    rules = dataset_service.get_cleaned_dataset_cleaning_rules(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )

    return Response(rules, media_type="application/json")