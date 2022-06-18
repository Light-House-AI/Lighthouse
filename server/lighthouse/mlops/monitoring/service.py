import json
from typing import Dict, List, Optional, Any
from .collections import DeploymentInput, DatasetExpectationsSuite
from .statistics import validate_original_data_with_new, generate_data_statistics


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


def get_project_input_data(project_id: int,
                           predicted_column_name: str,
                           skip: int = 0,
                           limit: int = 100) -> list:
    """
    Get unlabeled data for project.
    """
    input_data = DeploymentInput.objects(
        project_id=project_id).limit(limit).skip(skip)

    input_data_dict = [json.loads(row.to_json()) for row in input_data]

    return [{
        "id": row["_id"]["$oid"],
        predicted_column_name: row["primary_model_prediction"],
        "input_data": row["input_data"],
    } for row in input_data_dict]


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
            id=labeled_row["id"],
            project_id=project_id).update(set__label=labeled_row["label"])


def get_count_input_data(deployment_id: int) -> int:
    """
    Get number of input data for deployment.
    """
    return DeploymentInput.objects(deployment_id=deployment_id).count()


def save_dataset_expectations_suite(dataset_id: int,
                                    dataset_filename: str) -> int:
    """
    Save dataset expectations suite.
    """
    expectations_suite, _ = generate_data_statistics(dataset_filename,
                                                     str(dataset_id))

    dataset_expectations_suite = DatasetExpectationsSuite(
        dataset_id=dataset_id,
        expectations_suite=expectations_suite.to_json_dict(),
    )

    dataset_expectations_suite.save()
    return True


def get_deployment_monitoring_data(deployment_id: int,
                                   predicted_column_name: str) -> list:
    """
    Get deployment monitoring data.
    """
    input_data_dict = DeploymentInput.objects(
        deployment_id=deployment_id).to_json()

    formatted_input_data = [{
        predicted_column_name:
        row["primary_model_prediction"],
        **row["input_data"],
    } for row in input_data_dict]
