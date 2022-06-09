"""Celery task execution service"""

from celery import Celery
from lighthouse.config import config

celery_app = Celery(
    config.CELERY_APP_NAME,
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL,
)
