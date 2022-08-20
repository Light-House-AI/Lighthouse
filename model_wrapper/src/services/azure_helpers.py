from azure.storage.blob import BlobClient

from services.model_helpers import generate_model_storage_path


def download_blob(azure_conn_str: str, azure_container_name: str, azure_blob_name: str):
    try:
        download_file_path = generate_model_storage_path(
            azure_blob_name)
        blob_client = BlobClient.from_connection_string(
            azure_conn_str, azure_container_name, azure_blob_name)

        print(
            f"Downloading model {azure_blob_name} from the {azure_container_name} container...")

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print("Download is finished and file is stored as: " + download_file_path)
        return True

    except Exception as ex:
        print(ex)
        print(
            f"Blob {azure_blob_name} may not be found in the container. Recheck azure parameters")
        return False
