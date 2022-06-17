import json
from typing import Dict, List, Optional, Any
from .collections import DeploymentInput


def log_prediction(deployment_id: int,
                   project_id: int,
                   input_params: Dict[str, Any],
                   primary_model_prediction: str,
                   secondary_model_prediction: Optional[str] = None) -> None:
    """
    Adds a new deployment input to the database.
    """
    deployment_input = DeploymentInput(
        deployment_id=deployment_id,
        project_id=project_id,
        primary_model_prediction=primary_model_prediction,
        secondary_model_prediction=secondary_model_prediction,
        input_data=input_params,
    )

    deployment_input.save()


def get_project_input_data(project_id: int, skip: int = 0,
                           limit: int = 100) -> list:
    """
    Get unlabeled data for project.
    """
    return DeploymentInput.objects(
        project_id=project_id).limit(limit).skip(skip)


def get_project_labeled_input_data(project_id: int,
                                   predicted_column_name: str) -> list:
    """
    Get labeled data for project.
    """
    input_data = DeploymentInput.objects(
        project_id=project_id,
        label__exists=True,
    )

    input_data_dict = [json.loads(row.to_json()) for row in input_data]

    return [{
        **row["input_data"],
        predicted_column_name: row["label"],
    } for row in input_data_dict]


def label_input_data(project_id, labeled_data: List[Dict[str, str]]) -> None:
    """
    Label data.
    """
    for labeled_row in labeled_data:
        DeploymentInput.objects(
            id=labeled_row["oid"],
            project_id=project_id).update(set__label=labeled_row["label"])
