import os
from os.path import join, dirname
from dotenv import load_dotenv
import pickle

# TODO: Delete this function when there is no need for model_features_list
def convert_str_to_list(features_str: str):
    features_str = features_str.replace("[", "")
    features_str = features_str.replace("]", "")
    features_list = features_str.split(",")
    features_list = [float(feature) for feature in features_list]

    return features_list


def get_environment_variables():
    try:
        azure_storage_connection_string = os.environ.get(
            "AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.environ.get("CONTAINER_NAME")
        model_id = os.environ.get('MODEL_ID')
        environment_variables_dict = {}
        environment_variables_dict['azure_storage_connection_string'] = azure_storage_connection_string
        environment_variables_dict['container_name'] = container_name
        environment_variables_dict['model_id'] = model_id

        get_environment_variables_from_file(environment_variables_dict)

        return environment_variables_dict

    except Exception as ex:
        print("Missing one of the 3 required environment variables")
        print(ex)
        return None


# TODO: Delete this function when there is no need for model_features_list
def get_environment_variables_from_file(environment_variables_dict):
    folder_path = dirname(dirname(__file__))
    dotenv_path = join(folder_path, '.env')
    load_dotenv(dotenv_path)

    model_features_list = convert_str_to_list(os.getenv('MODEL_FEATURES_LIST'))
    environment_variables_dict['model_features_list'] = model_features_list


def generate_model_storage_path(model_id: str):
    #! FOR RUNNING WITHOUT DOCKER
    # models_folder_path = dirname(dirname(dirname(__file__))) + "/models/"
    #! FOR RUNNING WITH DOCKER
    models_folder_path = dirname(
        dirname(dirname(dirname(__file__)))) + "/models/"
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
