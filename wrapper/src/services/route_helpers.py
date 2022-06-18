import numpy as np
from typing import List

from services.model_helpers import load_pkl_model
from services.azure_helpers import download_blob


def greeting_fn():
    return {"Message":  f"Welcome to the ML WRAPPER API"}


def predict_for_deployment_type(environment_variables_dict, models_feature_list):
    azure_conn_str = environment_variables_dict['azure_storage_connection_string']
    azure_container_name = environment_variables_dict['azure_container_name']
    azure_main_blob_name = environment_variables_dict['azure_blob_name']
    deployment_type = environment_variables_dict['deployment_type']
    if deployment_type == "champion_challenger":
        azure_challenger_blob_name = environment_variables_dict['azure_blob_name_2']
        # is_downloaded = download_blob(azure_conn_str, azure_container_name,
        #                               azure_main_blob_name)
        # is_downloaded_2 = download_blob(azure_conn_str, azure_container_name,
        #                                 azure_challenger_blob_name)

        champion_prediction = predict_fn(azure_main_blob_name)
        challenger_prediction = predict_fn(azure_challenger_blob_name)
        return {"primary_prediction":  champion_prediction, "secondary_prediction": challenger_prediction}

    else:
        # is_downloaded = download_blob(azure_conn_str, azure_container_name,
        #                               azure_main_blob_name)
        if (True):
            prediction = predict_fn(azure_main_blob_name, models_feature_list)
            return {"primary_prediction":  prediction}


def predict_fn(azure_blob_name: str, models_feature_list: List[float]):
    # TODO models_feature_list will be removed
    model_features_list = np.array([models_feature_list])
    loaded_model = load_pkl_model(azure_blob_name)
    prediction = loaded_model.predict(model_features_list)
    #prediction = [np.argmax(predicted_value) for predicted_value in prediction]
    print(prediction)
    return prediction
