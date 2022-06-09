"""Contains the configuration for the application."""

from pydantic import BaseSettings

ENV_FILE_PATH = '.env'


class Config(BaseSettings):
    # Application name.
    APP_NAME: str = 'nn-generator'

    # Logging level.
    LOG_LEVEL: str = 'INFO'

    # Backend URL.
    RESULTS_BACKEND_URL: str = 'redis://:redispassword@localhost:6379/0'

    # Broker URL.
    BROKER_URL: str = 'redis://:redispassword@localhost:6379/0'

    # Webhook token.
    WEBHOOK_TOKEN: str = 'TEST_SECRET_DO_NOT_USE_IN_PROD'

    # Webhook URL.
    WEBHOOK_URL: str = 'http://localhost:8000/api/v1/models/{model_id}/training_status/'


config = Config(_env_file=ENV_FILE_PATH)
