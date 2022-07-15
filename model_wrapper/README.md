# Wrapper

## Functionality

- The wrapper repo will be used to

  1. Download model(s) from the azure storage container named models
  2. Expose the ML model to interact with it.
     - There is a predict router that retrieves the prediction of the model.
  3. Dockerize the service
  4. There are 3 deployments option
     - Single deployment (Default deployment)
     - Champion/Challenger deployment
     - Fallback deployment
  5. Parameters

     - AZURE_STORAGE_CONNECTION_STRING & AZURE_BLOB_NAME must be passed to docker
       - **AZURE_BLOB_NAME must not contain "." symbol**
     - AZURE_CONTAINER_NAME is optional with default value of "models"
     - DEPLOYMENT_ TYPE takes one of three values [None, "champion/challenger", "fallback"]


## How to run

- Dockerfile

  - Run default deployment mode (single)
    ```bash
    docker build -t ml_wrapper/fastapi .
    docker run -p 8000:8000 \
    --env AZURE_STORAGE_CONNECTION_STRING="value"\
    --env AZURE_CONTAINER_NAME=value\
    --env AZURE_BLOB_NAME=value\
    ml_wrapper/fastapi
    ```

  - Run other 2 modes
    ```bash
    docker build -t ml_wrapper/fastapi .
    docker run -p 8000:8000 \
    --env AZURE_STORAGE_CONNECTION_STRING="value"\
    --env AZURE_CONTAINER_NAME=value\
    --env DEPLOYMENT_TYPE=value\
    --env AZURE_BLOB_NAME=value\
    --env AZURE_BLOB_NAME_2=value\
    ml_wrapper/fastapi
    ```


- Run Docker Compose
  - Set the parameters in the .env.example and change the name to .env

  ```bash
  docker-compose up --build
  ```
