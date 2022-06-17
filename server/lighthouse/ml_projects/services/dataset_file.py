"""Dataset file service"""

import csv
import os
import shutil
from typing import BinaryIO, List
from azure.storage.blob import BlobClient
from lighthouse.config import config


def save_dicts_as_raw_dataset_file(dataset_id: int, dict_data: List[dict]):
    """
    Saves a list of dict as a raw dataset file.
    """
    file_path = get_raw_dataset_local_path(dataset_id)
    _save_dicts_to_csv(file_path, dict_data)
    return file_path


def _save_dicts_to_csv(file_path: str, dict_data: List[dict]):
    """
    Saves a list of dict data to csv file.
    """
    if len(dict_data) == 0:
        return

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=dict_data[0].keys())
        writer.writeheader()
        writer.writerows(dict_data)


def save_raw_dataset_to_local_disk(dataset_id: int, file: BinaryIO):
    """
    Saves a raw dataset to local disk.
    """
    file_path = get_raw_dataset_local_path(dataset_id)
    return save_file_to_local_disk(file_path, file)


def save_file_to_local_disk(file_path: str, file: BinaryIO):
    """
    Saves a file to local disk.
    """

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)

    file.close()
    return file_path


def upload_raw_dataset(dataset_id: int):
    """
    Uploads a raw dataset to Azure Blob Storage.
    """
    conn_str = config.AZURE_CONN_STR
    container_name = config.AZURE_RAW_DATASETS_CONTAINER_NAME

    blob_name = get_raw_dataset_blob_name(dataset_id)
    file_path = get_raw_dataset_local_path(dataset_id)

    return upload_blob(
        conn_str,
        container_name,
        blob_name,
        file_path,
    )


def upload_cleaned_dataset(dataset_id: int):
    """
    Uploads a cleaned dataset to Azure Blob Storage.
    """
    conn_str = config.AZURE_CONN_STR
    container_name = config.AZURE_CLEANED_DATASETS_CONTAINER_NAME

    blob_name = get_cleaned_dataset_blob_name(dataset_id)
    file_path = get_cleaned_dataset_local_path(dataset_id)

    return upload_blob(
        conn_str,
        container_name,
        blob_name,
        file_path,
    )


def upload_blob(conn_str: str, container_name: str, blob_name: str,
                file_path: str):
    """
    Uploads a blob to Azure Blob Storage.
    """
    blob = BlobClient.from_connection_string(
        conn_str=conn_str,
        container_name=container_name,
        blob_name=blob_name,
    )

    with open(file_path, "rb") as my_blob:
        blob.upload_blob(my_blob)

    return True


def download_cleaned_dataset(dataset_id: int):
    """
    Downloads a cleaned dataset from Azure Blob Storage.
    @return: dataset local path if the dataset was downloaded, empty string otherwise.
    """
    conn_str = config.AZURE_CONN_STR
    container_name = config.AZURE_CLEANED_DATASETS_CONTAINER_NAME

    blob_name = get_cleaned_dataset_blob_name(dataset_id)
    file_path = get_cleaned_dataset_local_path(dataset_id)

    return download_blob_if_not_exists(
        conn_str,
        container_name,
        blob_name,
        file_path,
    )


def download_raw_dataset(dataset_id: int):
    """
    Downloads a raw dataset from Azure Blob Storage.
    @return: dataset local path if the dataset was downloaded, empty string otherwise.
    """
    conn_str = config.AZURE_CONN_STR
    container_name = config.AZURE_RAW_DATASETS_CONTAINER_NAME

    blob_name = get_raw_dataset_blob_name(dataset_id)
    file_path = get_raw_dataset_local_path(dataset_id)

    return download_blob_if_not_exists(
        conn_str,
        container_name,
        blob_name,
        file_path,
    )


def download_blob_if_not_exists(conn_str: str, container_name: str,
                                blob_name: str, file_path: str):
    """
    Downloads a blob from Azure Blob Storage if it does not exist.
    """
    # check if the file already exists
    if os.path.isfile(file_path):
        return file_path

    # download the dataset
    download_blob(conn_str, container_name, blob_name, file_path)
    return file_path


def download_blob(conn_str: str, container_name: str, blob_name: str,
                  file_path: str):
    """
    Downloads a blob from Azure Blob Storage.
    """

    blob = BlobClient.from_connection_string(
        conn_str=conn_str,
        container_name=container_name,
        blob_name=blob_name,
    )

    with open(file_path, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

    return True


def get_raw_dataset_blob_name(dataset_id: int):
    """
    Returns the blob name of a raw dataset.
    """
    return f"{dataset_id}.csv"


def get_raw_dataset_local_path(dataset_id: int):
    """
    Returns the local path of a raw dataset.
    """
    return config.RAW_DATASETS_TEMP_DIR + f"/{dataset_id}.csv"


def get_cleaned_dataset_blob_name(dataset_id: int):
    """
    Returns the blob name of a cleaned dataset.
    """
    return f"{dataset_id}.csv"


def get_cleaned_dataset_local_path(dataset_id: int):
    """
    Returns the local path of a cleaned dataset.
    """
    return config.CLEANED_DATASETS_TEMP_DIR + f"/{dataset_id}.csv"


def create_directories():
    """
    Creates directories if they do not exist.
    """
    if not os.path.exists(config.RAW_DATASETS_TEMP_DIR):
        os.makedirs(config.RAW_DATASETS_TEMP_DIR)

    if not os.path.exists(config.CLEANED_DATASETS_TEMP_DIR):
        os.makedirs(config.CLEANED_DATASETS_TEMP_DIR)