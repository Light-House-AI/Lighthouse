"""Contains the configuration for the application."""

import os
from pydantic import BaseSettings

ENV_FILE_PATH = '.env'


class Config(BaseSettings):
    # Application name.
    APP_NAME: str = 'nn-generator'

    # Logging level.
    LOG_LEVEL: str = 'INFO'

    # Dramatiq broker URL.
    DRAMATIQ_REDIS_BROKER_URL: str = "redis://:redispassword@localhost:6379/0"

    # Models training queue name.
    MODELS_TRAINING_QUEUE_NAME: str = "train_model"

    # Webhook token.
    WEBHOOK_TOKEN: str = 'TEST_SECRET_DO_NOT_USE_IN_PROD'

    # Webhook URL.
    WEBHOOK_URL: str = 'http://localhost:8000/api/v1/models/{model_id}/training_status/'

    # Azure Blob Storage connection string.
    AZURE_CONN_STR: str = ''

    # Azure datasets container name.
    AZURE_DATASETS_CONTAINER_NAME: str = 'cleaned-datasets'

    # Azure models container name.
    AZURE_MODELS_CONTAINER_NAME: str = 'models'

    # Dataset temporary directory.
    DATASETS_TEMP_DIR: str = os.path.join(os.path.dirname(__file__),
                                          'tmp/raw_datasets/')

    # Models temporary directory.
    MODELS_TEMP_DIR: str = os.path.join(os.path.dirname(__file__),
                                        'tmp/models/')


config = Config(_env_file=ENV_FILE_PATH)
