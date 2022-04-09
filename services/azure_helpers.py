from azure.storage.blob import BlobClient

from model_helpers import get_environment_variables, generate_model_storage_path

environment_variables_dict = get_environment_variables()


def get_blob_client_from_connection_string(model_id):
    try:
        connection_string = environment_variables_dict['azure_storage_connection_string']
        container_name = environment_variables_dict['container_name']
        blob_client = BlobClient.from_connection_string(
            connection_string, container_name, model_id)

        return blob_client

    except Exception as ex:
        print(ex)
        print("Check connection string and/or container name")


def download_blob():
    try:
        container_name = environment_variables_dict['container_name']
        download_file_path = generate_model_storage_path()
        blob_name = download_file_path.split('/')[-1]
        blob_client = get_blob_client_from_connection_string(blob_name)

        print(
            f"Downloading model {blob_name} from the {container_name} container...")

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print("Download is finished and file is stored as: " + download_file_path)

    except Exception as ex:
        print(ex)
        print(f"Blob ({blob_name}) was not found in the container")


if __name__ == "__main__":
    download_blob()
