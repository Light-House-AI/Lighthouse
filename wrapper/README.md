# Wrapper

## Functionality

- The wrapper repo will be used to

  1. Download the model from the azure storage container named models
  2. Expose the ML model to interact with it.
     - There is a predict router that retrieves the classification of the model.
  3. Dockerize the service
  4. Parameters

     - AZURE_STORAGE_CONNECTION_STRING & AZURE_BLOB_NAME must be passed to docker
       - **AZURE_BLOB_NAME must not contain "." symbol**
     - AZURE_CONTAINER_NAME is optional with default value of "models"
     - model_features_list is taken from .env file (to be removed)

  5.

## How to run

- Run Docker file

  ```bash
  docker build -t wrapper/fastapi .
  docker run -p 8000:8000 \
   --env AZURE_STORAGE_CONNECTION_STRING="value"\
   --env AZURE_CONTAINER_NAME=value\
   --AZURE_BLOB_NAME=value\
   wrapper/fastapi
  ```

- Run Docker Compose

  ```bash
  docker-compose up --build
  ```
