from azure.storage.blob import BlobClient

from services.model_helpers import generate_model_storage_path


def download_blob(environment_variables_dict: dict):
    try:
        azure_container_name = environment_variables_dict['azure_container_name']
        azure_blob_name = environment_variables_dict['azure_blob_name']
        download_file_path = generate_model_storage_path(
            azure_blob_name)
        blob_name = download_file_path.split('/')[-1]
        blob_client = get_blob_client_from_connection_string(
            environment_variables_dict)

        print(
            f"Downloading model {blob_name} from the {azure_container_name} container...")

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print("Download is finished and file is stored as: " + download_file_path)

    except Exception as ex:
        print(ex)
        print(f"Blob ({blob_name}) was not found in the container")


def get_blob_client_from_connection_string(environment_variables_dict: dict):
    try:
        connection_string = environment_variables_dict['azure_storage_connection_string']
        azure_container_name = environment_variables_dict['azure_container_name']
        azure_blob_name = environment_variables_dict['azure_blob_name']
        blob_client = BlobClient.from_connection_string(
            connection_string, azure_container_name, azure_blob_name)

        return blob_client

    except Exception as ex:
        print(ex)
        print("Check connection string and/or container name")


# ? To run this main remove the services from model helpers and get "get env variables" fn
# if __name__ == "__main__":
#     download_blob(get_environment_variables())
