import requests
from sqlalchemy.orm import Session

from lighthouse.ml_projects.db import Deployment, Project
from lighthouse.mlops.monitoring import log_prediction


def get_prediction(*, user_id: str, deployment_id: str, input_data: dict,
                   db: Session):
    """
    Proxies to the deployed model to get predictions.
    Saves the request to the database.
    """

    # Get the deployment.
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id).join(
            Project, Project.user_id == user_id).first()

    if not deployment:
        raise Exception("Deployment not found!")

    if not deployment.is_running:
        raise Exception("Deployment is not running!")

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
