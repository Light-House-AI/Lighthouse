"""Router for Cleaned Datasets."""

from typing import List
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import cleaned_dataset as cleaned_dataset_service
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
    CleanedDatasetCreate,
    CleanedDatasetWithSources,
    CleanedDataset,
    DatasetCleaningRules,
)

router = APIRouter(prefix="/cleaned_datasets")


@router.get('',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[CleanedDataset])
@catch_app_exceptions
def get_cleaned_datasets(*,
                         project_id: int = Query(...),
                         skip: int = 0,
                         limit: int = 100,
                         db: Session = Depends(get_session),
                         user_data=Depends(get_current_user_data)):
    """
    Returns current user cleaned datasets.
    """
    return cleaned_dataset_service.get_cleaned_datasets(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('',
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
    return cleaned_dataset_service.create_cleaned_dataset(
        user_id=user_data.user_id,
        cleaned_dataset_in=cleaned_dataset_in,
        db=db,
    )


@router.get('/{dataset_id}',
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
    return cleaned_dataset_service.get_cleaned_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )


@router.get('/{dataset_id}/rows',
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
    rows = cleaned_dataset_service.get_cleaned_dataset_rows(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        skip=skip,
        limit=limit,
        db=db,
    )

    return Response(rows, media_type="application/json")


@router.get('/{dataset_id}/cleaning_rules',
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
    rules = cleaned_dataset_service.get_cleaned_dataset_cleaning_rules(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )

    return Response(rules, media_type="application/json")
