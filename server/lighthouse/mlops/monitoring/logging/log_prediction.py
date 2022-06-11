from typing import Any, Dict, Optional
from .collections import InputMetadata, DeploymentInput


def log_prediction(deployment_id: str,
                   input_params: Dict[str, Any],
                   primary_model_prediction: str,
                   secondary_model_prediction: Optional[str] = None) -> None:
    """
    Adds a new deployment input to the database.
    """
    # Create the input metadata.
    input_metadata = InputMetadata(
        deployment_id=deployment_id,
        primary_model_prediction=primary_model_prediction,
        secondary_model_prediction=secondary_model_prediction,
    )

    # Create the deployment input.
    deployment_input = DeploymentInput(
        **input_params,
        _metadata=input_metadata,
    )

    # Save the deployment input.
    deployment_input.save()