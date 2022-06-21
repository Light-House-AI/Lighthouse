"""
Contains the configuration for the application.
"""

import os
from pydantic import BaseSettings

ENV_FILE_PATH = '.env'


class Config(BaseSettings):
    # Application environment
    ENVIRONMENT: str = 'prod'

    # Enable debug mode.
    DEBUG: bool = False

    # The logging level.
    LOG_LEVEL: str = 'INFO'

    # The database URL.
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'

    # Grabs the folder where the script runs.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Temporary raw datasets location.
    RAW_DATASETS_TEMP_DIR = os.path.join(os.path.dirname(BASE_DIR),
                                         'tmp\\raw_datasets')

    # Temporary cleaned datasets location.
    CLEANED_DATASETS_TEMP_DIR = os.path.join(os.path.dirname(BASE_DIR),
                                             'tmp\\cleaned_datasets')

    # Azure Blob Storage connection string.
    AZURE_CONN_STR: str = ''

    # Azure cleaned datasets container name.
    AZURE_CLEANED_DATASETS_CONTAINER_NAME: str = 'cleaned-datasets'

    # Azure raw datasets container name.
    AZURE_RAW_DATASETS_CONTAINER_NAME: str = 'raw-datasets'

    # Access token expiration time (in minutes).
    # 8 days in minutes = 8 * 24 * 60 = 86400
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Access token secret key.
    ACCESS_TOKEN_SECRET_KEY: str = 'TEST_SECRET_DO_NOT_USE_IN_PROD'

    # The JWT algorithm.
    JWT_ALGORITHM: str = 'HS256'

    # Backend CORS origin.
    CORS_ORIGIN = ["http://localhost:8000"]

    # Quantity of workers for uvicorn.
    WORKERS_COUNT: int = 1

    # Enable uvicorn reloading.
    RELOAD: bool = False

    # Host for uvicorn.
    HOST: str = "0.0.0.0"

    # Port for uvicorn.
    PORT: int = 8000

    # Base URL for API.
    API_PREFIX: str = "/api/v1"

    # Login route.
    LOGIN_ROUTE: str = "/api/v1/auth/login"

    # Monitoring MongoDB URL.
    MONITORING_MONGO_URI: str = "mongodb://localhost:27017/monitoring"

    # Monitoring MongoDB Alias.
    MONITORING_MONGO_ALIAS: str = "monitoring"

    # ML-Projects MongoDB URL.
    ML_PROJECTS_MONGO_URI: str = "mongodb://localhost:27017/ml_projects"

    # ML-Projects MongoDB Alias.
    ML_PROJECTS_MONGO_ALIAS: str = "ml-projects"

    # Celery app name.
    CELERY_APP_NAME: str = "light-house"

    # Dramatiq broker URL.
    DRAMATIQ_REDIS_BROKER_URL: str = "redis://:redispassword@localhost:6379/0"

    # Models training queue name.
    MODELS_TRAINING_QUEUE_NAME: str = "train_model"

    # Webhook Token.
    WEBHOOK_TOKEN: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"

    # Github containers registry username.
    GHCR_USERNAME: str = ""

    # Github containers registry password.
    GHCR_PASSWORD: str = ""

    # Monitoring rows threshold.
    MONITORING_NUM_ROWS_NOTIFY: int = 10


config = Config(_env_file=ENV_FILE_PATH)
