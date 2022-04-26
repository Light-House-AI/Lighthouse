import os
from os.path import join, dirname
from dotenv import load_dotenv
import pickle


def convert_str_to_list(features_str: str):
    features_str = features_str.replace("[", "")
    features_str = features_str.replace("]", "")
    features_list = features_str.split(",")
    features_list = [float(feature) for feature in features_list]

    return features_list


def get_environment_variables():
    folder_path = dirname(dirname(__file__))
    dotenv_path = join(folder_path, '.env')
    load_dotenv(dotenv_path)

    azure_storage_connection_string = os.environ.get(
        "AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("CONTAINER_NAME")
    model_id = os.getenv('MODEL_ID')
    model_features_list = convert_str_to_list(os.getenv('MODEL_FEATURES_LIST'))

    environment_variables_dict = {}
    environment_variables_dict['azure_storage_connection_string'] = azure_storage_connection_string
    environment_variables_dict['container_name'] = container_name
    environment_variables_dict['model_id'] = model_id
    environment_variables_dict['model_features_list'] = model_features_list

    return environment_variables_dict


def generate_model_storage_path(model_id: str):
    models_folder_path = dirname(dirname(dirname(__file__))) + "/models/"
    download_file_path = models_folder_path + model_id

    return download_file_path


def load_pkl_model(model_id: str):
    try:
        model_path = generate_model_storage_path(model_id)
        pickle_in = open(model_path, 'rb')
        model = pickle.load(pickle_in)
        return model
    except Exception as ex:
        print(ex)
        print("Extension may not .pkl")
        return None


# if __name__ == "__main__":
#     print(get_environment_variables())
#     print(load_pkl_model("classifier1.0.pkl"))
