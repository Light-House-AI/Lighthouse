"""Deployment service."""

import requests
from sqlalchemy.orm import Session

from lighthouse.mlops.monitoring import log_prediction
from lighthouse.ml_projects.schemas import DeploymentCreate

from lighthouse.ml_projects.exceptions import (
    NotFoundException,
    BadRequestException,
)

from lighthouse.ml_projects.db import (Model, Deployment, DeploymentType,
                                       Project)


def get_deployments(user_id: str, skip: int, limit: int, db: Session):
    """
    Gets all deployments.
    """
    return db.query(Deployment).join(
        Project, Project.user_id == user_id).offset(skip).limit(limit).all()


def get_deployment(user_id: str, deployment_id: int, db: Session):
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
                      db: Session):
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

    # Create deployment
    print(deployment_data.type)
    print("haa       ", deployment_data.dict())
    deployment = Deployment(**deployment_data.dict())
    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    # TODO: Call create deployment

    return deployment


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
