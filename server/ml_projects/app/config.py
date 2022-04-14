"""
Contains the configuration for the application.
"""

import os
from pydantic import BaseSettings

ENV_FILE_PATH = 'ml_projects/.env'


class Config(BaseSettings):
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
    CORS_ORIGIN: str = "*"


config = Config(_env_file=ENV_FILE_PATH)
