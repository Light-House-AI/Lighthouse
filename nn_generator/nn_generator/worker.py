import random
import time

import requests
from celery import Celery
from celery.utils.log import get_logger

from .config import config

app = Celery(
    config.APP_NAME,
    broker=config.BROKER_URL,
    backend=config.RESULTS_BACKEND_URL,
)

logger = get_logger(__name__)
logger.setLevel(config.LOG_LEVEL)


@app.task(name='train_model')
def run_train_model_task(model_id: str, dataset_id: str,
                         predicted_column: str):
    """
    Trains a model and notifies the server when it is finished.
    """
    logger.info(f'Training model {model_id}')

    train_model(model_id, dataset_id, predicted_column)
    notify_finished(model_id)

    logger.info(f'Finished training model {model_id}')
    return True


def train_model(model_id: str, dataset_id: str, predicted_column: str):
    """
    Trains a model.
    """
    time.sleep(10 * random.random())  # Simulate a long task


def notify_finished(model_id: str):
    """
    Sends a notification to the server that the model is finished.
    """
    requests.post(config.WEBHOOK_URL.format(model_id=model_id),
                  headers={'x-token': config.WEBHOOK_TOKEN})


def start_worker():
    """
    Starts the worker.
    """
    worker = app.Worker()
    worker.start()