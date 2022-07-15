"""Router for Raw Datasets."""

from typing import List, Dict
from fastapi import APIRouter, Depends, Query, UploadFile, Response
from sqlalchemy.orm import Session

from lighthouse.ml_projects.services import raw_dataset as raw_dataset_service
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
    RawDataset,
)

router = APIRouter(prefix="/raw_datasets")


@router.get('',
            responses=UnauthenticatedException.get_example_response(),
            response_model=List[RawDataset])
@catch_app_exceptions
def get_raw_datasets(*,
                     project_id: int = Query(...),
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_session),
                     user_data=Depends(get_current_user_data)):
    """
    Returns current user raw datasets.
    """
    return raw_dataset_service.get_raw_datasets(
        user_id=user_data.user_id,
        project_id=project_id,
        db=db,
        skip=skip,
        limit=limit,
    )


@router.post('',
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
    return raw_dataset_service.create_raw_dataset(
        user_id=user_data.user_id,
        raw_dataset_in=raw_dataset_in,
        db=db,
    )


@router.get('/recommendations',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            },
            response_model=Dict[str, List[Dict]])
@catch_app_exceptions
def get_raw_dataset_cleaning_rules_recommendations(
        *,
        datasets_ids: List[int] = Query([], alias="datasets_ids[]"),
        db: Session = Depends(get_session),
        user_data=Depends(get_current_user_data)):
    """
    Returns raw dataset cleaning rules recommendations.
    """
    result = raw_dataset_service.get_raw_dataset_cleaning_rules_recommendations(
        user_id=user_data.user_id,
        datasets_ids=datasets_ids,
        db=db,
    )

    return Response(result, media_type="application/json")


@router.get('/{dataset_id}',
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
    return raw_dataset_service.get_raw_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )


@router.post('/{dataset_id}/upload',
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
    return raw_dataset_service.upload_raw_dataset(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        file=file,
        db=db,
    )


@router.get('/{dataset_id}/rows',
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
    rows = raw_dataset_service.get_raw_dataset_rows(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        skip=skip,
        limit=limit,
        db=db,
    )

    return Response(rows, media_type="application/json")


@router.get('/{dataset_id}/visualizations',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
@catch_app_exceptions
def get_raw_dataset_visualizations(*,
                                   dataset_id: int,
                                   columns: List[str] = Query(
                                       [], alias="columns[]"),
                                   db: Session = Depends(get_session),
                                   user_data=Depends(get_current_user_data)):
    """
    Returns raw dataset visualizations.
    """
    return raw_dataset_service.get_raw_dataset_visualization(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        columns=columns,
        db=db,
    )


@router.get('/{dataset_id}/correlation',
            responses={
                **UnauthenticatedException.get_example_response(),
                **NotFoundException.get_example_response(),
            })
@catch_app_exceptions
def get_raw_dataset_correlation(*,
                                dataset_id: int,
                                db: Session = Depends(get_session),
                                user_data=Depends(get_current_user_data)):
    """
    Returns raw dataset features correlation.
    """
    return raw_dataset_service.get_raw_dataset_correlation(
        user_id=user_data.user_id,
        dataset_id=dataset_id,
        db=db,
    )


@router.post('/shadow_data',
             responses=UnauthenticatedException.get_example_response())
@catch_app_exceptions
def create_raw_dataset_from_shadow_data(
        *,
        raw_dataset_in: RawDatasetCreate,
        db: Session = Depends(get_session),
        user_data=Depends(get_current_user_data)):
    """
    Creates a raw dataset from shadow data.
    """
    return raw_dataset_service.create_raw_dataset_from_project_shadow_data(
        user_id=user_data.user_id,
        raw_dataset_in=raw_dataset_in,
        db=db,
    )