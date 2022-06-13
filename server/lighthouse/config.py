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

    # MongoDB URL.
    MONGO_URI: str = "mongodb://localhost:27017/"


config = Config(_env_file=ENV_FILE_PATH)
