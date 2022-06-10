import os
import shutil
from typing import BinaryIO
from azure.storage.blob import BlobClient
from lighthouse.config import config


def save_raw_dataset_to_local_disk(dataset_id: int, file: BinaryIO):
    """
    Saves a raw dataset to local disk.
    """
    file_path = config.RAW_DATASETS_TEMP_DIR + f"/{dataset_id}.csv"
    return save_file_to_local_disk(file_path, file)


def save_file_to_local_disk(file_path: str, file: BinaryIO):
    """
    Saves a file to local disk.
    """

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        file.close()
        return True

    except Exception as ex:
        print(ex)
        file.close()
        return False


def upload_raw_dataset(dataset_id: int):
    """
    Uploads a raw dataset to Azure Blob Storage.
    """
    conn_str = config.AZURE_CONN_STR
    container_name = config.AZURE_raw_DATASETS_CONTAINER_NAME

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
    try:
        blob = BlobClient.from_connection_string(
            conn_str=conn_str,
            container_name=container_name,
            blob_name=blob_name,
        )

        with open(file_path, "rb") as my_blob:
            blob.upload_blob(my_blob)

        return True
    except Exception as ex:
        print(ex)
        return False


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
    is_downloaded = download_blob(conn_str, container_name, blob_name,
                                  file_path)

    if is_downloaded:
        return file_path
    else:
        return ""


def download_blob(conn_str: str, container_name: str, blob_name: str,
                  file_path: str):
    """
    Downloads a blob from Azure Blob Storage.
    """
    try:
        blob = BlobClient.from_connection_string(
            conn_str=conn_str,
            container_name=container_name,
            blob_name=blob_name,
        )

        with open(file_path, "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)

    except Exception as ex:
        print(ex)
        return False


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