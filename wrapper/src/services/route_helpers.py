from services.model_helpers import load_pkl_model
from services.azure_helpers import download_blob


def greeting_fn():
    return {"Message":  f"Welcome to the ML WRAPPER API"}


def predict_for_deployment_type(environment_variables_dict):
    azure_conn_str = environment_variables_dict['azure_storage_connection_string']
    azure_container_name = environment_variables_dict['azure_container_name']
    azure_main_blob_name = environment_variables_dict['azure_blob_name']
    deployment_type = environment_variables_dict['deployment_type']
    if deployment_type == "champion_challenger" or deployment_type == "ch/ch":
        azure_challenger_blob_name = environment_variables_dict['azure_blob_name_2']
        is_downloaded = download_blob(azure_conn_str, azure_container_name,
                                      azure_main_blob_name)
        is_downloaded_2 = download_blob(azure_conn_str, azure_container_name,
                                        azure_challenger_blob_name)
        if is_downloaded and is_downloaded_2:
            champion_prediction = predict_fn(azure_main_blob_name)
            challenger_prediction = predict_fn(azure_challenger_blob_name)
            # TODO both predictions to be saved in the database
            return {"Champion Prediction ":  f"{champion_prediction}"}

    elif deployment_type == "fallback":
        return "FALLBACK"

    else:
        is_downloaded = download_blob(azure_conn_str, azure_container_name,
                                      azure_main_blob_name)
        if (is_downloaded):
            return predict_fn(azure_main_blob_name)


def predict_fn(azure_blob_name: str):
    # TODO models_feature_list will be removed
    model_features_list = [1, 2, 3, 4]
    loaded_model = load_pkl_model(azure_blob_name)
    prediction = loaded_model.predict([model_features_list])
    return prediction[0]


def save_prediction():
    pass


def train_fn():
    pass
