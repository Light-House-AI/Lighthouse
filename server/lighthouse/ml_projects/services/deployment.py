"""Deployment service."""

import requests
from typing import Dict
from sqlalchemy.orm import Session

from lighthouse.config import config
from lighthouse.mlops.monitoring.logging import service as monitoring_service
from lighthouse.ml_projects.schemas import DeploymentCreate

from lighthouse.ml_projects.exceptions import (
    NotFoundException,
    BadRequestException,
)

from lighthouse.ml_projects.db import (
    Model,
    Deployment,
    Project,
    Notification,
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
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id).join(
            Project, Project.user_id == user_id).first()

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
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id).join(
            Project, Project.user_id == user_id).first()

    if not deployment:
        raise NotFoundException("Deployment not found!")

    if not deployment.is_running:
        raise BadRequestException("Deployment is not running!")

    # Get the predictions from the deployed model.
    url = str(deployment_id) + "/predict"

    # TODO: uncomment line below
    # deployment_response = requests.get(url, json=input_data).json()

    # TODO: delete the dummy data below
    deployment_response = {
        "primary_model_prediction": "primary_prediction",
        "secondary_model_prediction": "secondary_prediction",
    }

    # Save the request to the database.
    monitoring_service.log_prediction(
        deployment_id=deployment_id,
        project_id=deployment.project_id,
        input_params=input_data,
        primary_model_prediction=deployment_response[
            "primary_model_prediction"],
        secondary_model_prediction=deployment_response[
            "secondary_model_prediction"],
    )

    # Check for statistics monitoring
    _notify_for_monitoring(deployment, user_id, db)

    # Return the predictions.
    deployment_response["predictions"] = deployment_response.pop(
        "primary_model_prediction")

    deployment_response.pop("secondary_model_prediction")

    return deployment_response


def _notify_for_monitoring(deployment: Deployment, user_id: int, db: Session):
    """
    Notifies the monitoring service about a deployment.
    """
    if deployment.has_monitoring_notification:
        return

    num_input_data = monitoring_service.get_count_input_data(
        deployment_id=deployment.id)

    print("num_input_data:", num_input_data)
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
