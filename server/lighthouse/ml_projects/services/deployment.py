"""Deployment service."""

import json
import requests
import numpy as np
import pandas as pd

from typing import Dict
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from lighthouse.config import config
from lighthouse.mlops.monitoring import service as monitoring_service
from lighthouse.ml_projects.services import dataset_file as dataset_file_service
from lighthouse.automl.data_cleaning import service as data_cleaning_service
from lighthouse.automl import feature_engineering as feature_engineering_service

from lighthouse.ml_projects.schemas import DeploymentCreate

from lighthouse.ml_projects.mongo import (
    ProjectDataColumns,
    DatasetCleaningRules,
    DatasetFeatureRules,
)

from lighthouse.ml_projects.exceptions import (
    NotFoundException,
    BadRequestException,
)

from lighthouse.ml_projects.db import (
    Model,
    Deployment,
    Project,
    Notification,
    CleanedDataset,
    CleanedDatasetSource,
)

from lighthouse.mlops.serving import (
    recreate_ingress_rules,
    add_main_ingress_path,
    deploy_model,
    delete_model,
    startup,
)


def init_serving_module(db: Session):
    """
    Initializes the serving module.
    """
    add_main_ingress_path()
    config_dict = startup()

    # Get deployments.
    deployments = db.query(
        Deployment.id).filter(Deployment.is_running == True).all()

    deployments_ids = [
        _get_k8s_deployment_name(deployment[0]) for deployment in deployments
    ]

    # Initialize module.
    recreate_ingress_rules(config_dict, deployments_ids)

    return config_dict


def _get_k8s_deployment_name(deployment_id: int):
    """
    Gets the k8s deployment name.
    """
    return "lighthouse-{}".format(deployment_id)


def get_deployments(user_id: int, project_id: int, skip: int, limit: int,
                    db: Session):
    """
    Gets all deployments.
    """
    return db.query(Deployment).join(Project).filter(
        Project.user_id == user_id,
        Project.id == project_id).offset(skip).limit(limit).all()


def get_deployment(user_id: int, deployment_id: int, db: Session):
    """
    Gets a deployment.
    """
    deployment = db.query(Deployment). \
        filter(Deployment.id == deployment_id). \
        join(Project, Project.user_id == user_id). \
        outerjoin(Model, or_(Model.id == Deployment.primary_model_id,
                             Model.id == Deployment.secondary_model_id)). \
        options(joinedload(Deployment.primary_model)). \
        options(joinedload(Deployment.secondary_model)). \
        first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    return deployment


def create_deployment(user_id: int, deployment_data: DeploymentCreate,
                      serving_config: Dict, db: Session):
    """
    Creates a deployment.
    """

    # Check that project exists
    project_exists = db.query(Project).filter(
        Project.user_id == user_id,
        Project.id == deployment_data.project_id).count()

    if not project_exists:
        raise NotFoundException("Project not found.")

    # Check if models exists
    if deployment_data.secondary_model_id:
        num_models = db.query(Model).join(Project).filter(
            Project.user_id == user_id,
            Model.id.in_([
                deployment_data.primary_model_id,
                deployment_data.secondary_model_id
            ])).count()

        if num_models != 2:
            raise BadRequestException("Invalid model ids.")

    else:
        models_exists = db.query(Model).join(Project).filter(
            Model.id == deployment_data.primary_model_id,
            Project.user_id == user_id).count()

        if not models_exists:
            raise NotFoundException("Model not found.")

    # Create deployment record
    deployment = Deployment(**deployment_data.dict())
    db.add(deployment)
    db.commit()

    # Create deployment
    _deploy(deployment, serving_config)
    deployment.is_running = True
    db.commit()

    return deployment


def run_deployment(user_id: int, deployment_id: int, serving_config: Dict,
                   db: Session):
    """
    Starts a deployment.
    """

    # Get the deployment.
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id).join(
            Project, Project.user_id == user_id).first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    if deployment.is_running:
        raise BadRequestException("Deployment is already running!")

    # Start the deployment.
    _deploy(deployment, serving_config)
    deployment.is_running = True
    db.commit()

    return deployment


def _deploy(deployment: Deployment, serving_config: Dict):
    """
    Deploys a deployment.
    """
    return deploy_model(
        serving_config,
        _get_k8s_deployment_name(deployment.id),
        deployment.type.value,
        str(deployment.primary_model_id),
        str(deployment.secondary_model_id),
    )


def stop_deployment(user_id: int, deployment_id: int, serving_config: Dict,
                    db: Session):
    """
    Stops a deployment.
    """

    # Get the deployment.
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id).join(
            Project, Project.user_id == user_id).first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    if not deployment.is_running:
        raise BadRequestException("Deployment is not running!")

    # Delete the deployment.
    delete_model(serving_config, _get_k8s_deployment_name(deployment.id))
    deployment.is_running = False
    db.commit()

    return deployment


def get_prediction(*, user_id: int, deployment_id: int, input_data: dict,
                   db: Session):
    """
    Proxies to the deployed model to get predictions.
    Saves the request to the database.
    
    :raises: NotFoundException, BadRequestException
    """

    # Get the deployment.
    deployment = db.query(Deployment). \
        filter(Deployment.id == deployment_id). \
        join(Project, Project.user_id == user_id). \
        join(Model). \
        join(CleanedDataset). \
        outerjoin(CleanedDatasetSource). \
        options(joinedload(Deployment.primary_model, Model.dataset,
                            CleanedDataset.sources)). \
        options(joinedload(Deployment.project)). \
        first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    if not deployment.is_running:
        raise BadRequestException("Deployment is not running!")

    # Get deployment info
    project_id = deployment.project.id
    dataset_id = deployment.primary_model.dataset_id
    predicted_column = deployment.project.predicted_column

    # Get datasets
    raw_datasets_file_paths = [
        dataset_file_service.download_raw_dataset(dataset.raw_dataset_id)
        for dataset in deployment.primary_model.dataset.sources
    ]

    merged_dataset_filepath, _ = dataset_file_service.get_temporary_dataset_local_path(
    )

    merged_dataset_df = data_cleaning_service.create_save_merged_dataframe(
        raw_datasets_file_paths, merged_dataset_filepath)

    # Sort columns
    project_schema = ProjectDataColumns.objects(project_id=project_id).first()
    ordered_input_data = {}
    for column in project_schema.columns:
        if column == predicted_column:
            continue

        ordered_input_data[column] = input_data.get(column)

    # Clean data
    cleaning_rules = DatasetCleaningRules.objects(
        dataset_id=dataset_id).first().rules

    cleaned_data = data_cleaning_service.get_cleaned_input_data(
        input_data=ordered_input_data,
        rules=cleaning_rules,
        raw_data=merged_dataset_df,
        predicted_column=predicted_column,
    )

    # Get features
    features_rules = DatasetFeatureRules.objects(
        dataset_id=dataset_id).first().rules

    features_data = feature_engineering_service.apply_FE_rules(
        cleaned_data,
        features_rules,
    )

    # Get the predictions from the deployed model.
    request_data = _features_to_numpy_string(features_data)
    url = _get_deployment_predict_url(deployment_id)
    deployment_response = requests.post(url, data=request_data).json()

    # Save the request to the database.
    primary_prediction = deployment_response.get("primary_prediction")
    secondary_prediction = deployment_response.get("secondary_prediction")

    monitoring_service.log_prediction(
        deployment_id=deployment_id,
        project_id=deployment.project_id,
        input_params=input_data,
        primary_model_prediction=primary_prediction,
        secondary_model_prediction=secondary_prediction,
    )

    # Check for statistics monitoring
    _notify_for_monitoring(deployment, user_id, db)

    return {
        "primary_prediction": primary_prediction,
        "secondary_prediction": secondary_prediction
    }


def _features_to_numpy_string(features: pd.DataFrame):
    features_np = features.to_numpy()
    result = np.array2string(
        features_np,
        separator=',',
        formatter={'float_kind': lambda x: "%.10f" % x},
    )

    return result


def _get_deployment_predict_url(deployment_id: int):
    """
    Gets the deployment url.
    """
    return config.DOMAIN_URL + "/" + _get_k8s_deployment_name(
        deployment_id) + "/predict"


def _notify_for_monitoring(deployment: Deployment, user_id: int, db: Session):
    """
    Notifies the monitoring service about a deployment.
    """
    if deployment.has_monitoring_notification:
        return

    num_input_data = monitoring_service.get_count_input_data(
        deployment_id=deployment.id)

    if num_input_data < config.MONITORING_NUM_ROWS_NOTIFY:
        return

    notification = Notification(
        user_id=user_id,
        title="Deployment monitoring",
        body="Deployment \"" + deployment.name +
        "\" may have some data drift.",
    )

    db.add(notification)
    deployment.has_monitoring_notification = True
    db.commit()


def get_monitoring_data(user_id: int, deployment_id: int, db: Session):
    """
    Gets the monitoring data for a deployment.
    """

    # Get the deployment.
    deployment = db.query(Deployment). \
        filter(Deployment.id == deployment_id). \
        join(Project, Project.user_id == user_id). \
        join(Model, Model.id == Deployment.primary_model_id). \
        options(joinedload(Deployment.primary_model)). \
        options(joinedload(Deployment.project)). \
        first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    # Get input data
    deployment_input_data = monitoring_service.get_deployment_input_data(
        deployment_id=deployment.id,
        predicted_column_name=deployment.project.predicted_column,
    )

    # Save input data to temporary file
    temp_dataset_file_path, temp_dataset_filename = dataset_file_service.get_temporary_dataset_local_path(
    )

    dataset_file_service._save_dicts_to_csv(
        temp_dataset_file_path,
        deployment_input_data,
    )

    # Get monitoring results
    result = monitoring_service.get_deployment_monitoring_data(
        dataset_id=deployment.primary_model.dataset_id,
        dataset_file_name=temp_dataset_filename,
    )

    # Delete temporary file
    dataset_file_service.delete_file(temp_dataset_file_path)

    return result