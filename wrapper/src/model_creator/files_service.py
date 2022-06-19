"""Files service."""

import os
import pandas as pd
from azure.storage.blob import BlobClient
from .config import config


def create_directories():
    """
    Creates directories if they do not exist.
    """
    if not os.path.exists(config.MODELS_TEMP_DIR):
        os.makedirs(config.MODELS_TEMP_DIR)

    if not os.path.exists(config.DATASETS_TEMP_DIR):
        os.makedirs(config.DATASETS_TEMP_DIR)


def download_dataset(dataset_id: int):
    """
    Downloads a dataset from Azure Blob Storage.
    """
    file_path = get_dataset_local_path(dataset_id)

    if os.path.isfile(file_path):
        return file_path

    # download the dataset
    blob_name = get_dataset_blob_name(dataset_id)
    blob = BlobClient.from_connection_string(
        conn_str=config.AZURE_CONN_STR,
        container_name=config.AZURE_DATASETS_CONTAINER_NAME,
        blob_name=blob_name,
    )

    with open(file_path, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

    return file_path


def get_dataset_data_frame(dataset_path: str):
    """
    Returns a data frame of a dataset.
    """
    return pd.read_csv(dataset_path)


def upload_model(model_id: int):
    """
    Uploads a model to Azure Blob Storage.
    """
    # create upload client
    blob_name = get_model_blob_name(model_id)
    blob = BlobClient.from_connection_string(
        conn_str=config.AZURE_CONN_STR,
        container_name=config.AZURE_MODELS_CONTAINER_NAME,
        blob_name=blob_name,
    )

    # upload the model
    file_path = get_model_local_path(model_id)
    with open(file_path, "rb") as my_blob:
        blob.upload_blob(my_blob)

    return True


def delete_dataset_local_file(dataset_id: int):
    """
    Deletes a dataset from local storage.
    """
    file_path = get_dataset_local_path(dataset_id)
    if os.path.isfile(file_path):
        os.remove(file_path)


def delete_model_local_file(model_id: int):
    """
    Deletes a model from local storage.
    """
    file_path = get_model_local_path(model_id)
    if os.path.isfile(file_path):
        os.remove(file_path)


def get_dataset_local_path(dataset_id: int):
    """
    Returns the local path of a dataset.
    """
    return config.DATASETS_TEMP_DIR + get_dataset_blob_name(dataset_id)


def get_dataset_blob_name(dataset_id: int):
    """
    Returns the blob name of a dataset.
    """
    return f"{dataset_id}.csv"


def get_model_local_path(model_id: int):
    """
    Returns the local path of a model.
    """
    return config.MODELS_TEMP_DIR + get_model_blob_name(model_id)


def get_model_blob_name(model_id: int):
    """
    Returns the blob name of a model.
    """
    return f"{model_id}.pkl"
