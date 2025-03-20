import os
from os.path import dirname
import pickle


def get_environment_variables():
    try:
        environment_variables_dict = {}
        deployment_type = os.environ['DEPLOYMENT_TYPE']
        if deployment_type is None or deployment_type is "single":
            deployment_type = "single"
        else:
            environment_variables_dict["azure_blob_name_2"] = os.environ['AZURE_BLOB_NAME_2']

        environment_variables_dict['azure_storage_connection_string'] = os.environ.get(
            "AZURE_STORAGE_CONNECTION_STRING")
        environment_variables_dict['azure_container_name'] = os.environ.get(
            "AZURE_CONTAINER_NAME")
        environment_variables_dict['azure_blob_name'] = os.environ.get(
            'AZURE_BLOB_NAME')
        environment_variables_dict['deployment_type'] = deployment_type

        return environment_variables_dict

    except Exception as ex:
        print("Error in one of the sent environment variables")
        print(ex)
        return None


def load_pkl_model(azure_blob_name: str):
    try:
        model_path = generate_model_storage_path(azure_blob_name)
        pickle_in = open(model_path, 'rb')
        model = pickle.load(pickle_in)
        return model
    except Exception as ex:
        print(ex)
        print("Extension may not .pkl")
        return None


def generate_model_storage_path(azure_blob_name: str):
    #! FOR RUNNING WITHOUT DOCKER
    # models_folder_path = dirname(
    #     dirname(dirname(__file__))) + "/models/"
    #! FOR RUNNING WITH DOCKER
    models_folder_path = dirname(
        dirname(dirname(dirname(__file__)))) + "/models/"
    download_file_path = models_folder_path + azure_blob_name
    return download_file_path
