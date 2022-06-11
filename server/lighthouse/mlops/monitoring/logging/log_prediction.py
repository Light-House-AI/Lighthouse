from typing import Any, Dict, Optional
from .collections import InputData, DeploymentInput


def log_prediction(deployment_id: str,
                   input_params: Dict[str, Any],
                   primary_model_prediction: str,
                   secondary_model_prediction: Optional[str] = None) -> None:
    """
    Adds a new deployment input to the database.
    """
    deployment_input = DeploymentInput(
        deployment_id=deployment_id,
        primary_model_prediction=primary_model_prediction,
        secondary_model_prediction=secondary_model_prediction,
        input_data=input_params,
    )

    deployment_input.save()