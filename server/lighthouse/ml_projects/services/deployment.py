"""Deployment service."""

import requests
from sqlalchemy.orm import Session

from lighthouse.ml_projects.db import Deployment, Project
from lighthouse.mlops.monitoring import log_prediction

from lighthouse.ml_projects.exceptions import (
    NotFoundException,
    BadRequestException,
)


def get_prediction(*, user_id: str, deployment_id: int, input_data: dict,
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
    url = deployment_id + "/predict"

    # TODO: uncomment line below
    # deployment_response = requests.get(url, json=input_data).json()

    # TODO: delete the dummy data below
    deployment_response = {
        "primary_model_prediction": "primary_prediction",
        "secondary_model_prediction": "secondary_prediction",
    }

    # Save the request to the database.
    log_prediction(
        deployment_id=deployment_id,
        input_params=input_data,
        primary_model_prediction=deployment_response[
            "primary_model_prediction"],
        secondary_model_prediction=deployment_response[
            "secondary_model_prediction"],
    )

    # Return the predictions.
    deployment_response["predictions"] = deployment_response.pop(
        "primary_model_prediction")

    deployment_response.pop("secondary_model_prediction")

    return deployment_response


def create_deployment(project_id: int, model_id: int, db: Session):
    """
    Creates a deployment.
    """
    deployment = Deployment(project_id=project_id, model_id=model_id)
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment
