"""Worker functions"""

import requests
from typing import Dict

import dramatiq
from dramatiq import get_logger
from dramatiq.brokers.redis import RedisBroker

from model_creator.neural_network import NetworkGenerator, export_model
from model_fit_generator.config import config
import model_fit_generator.files_service as files_service

# init dramatiq
dramatiq.set_broker(RedisBroker(url=config.DRAMATIQ_REDIS_BROKER_URL))

# init logger
logger = get_logger(__name__)
logger.setLevel(config.LOG_LEVEL)

# create directories
files_service.create_directories()


@dramatiq.actor(
    queue_name=config.MODELS_TRAINING_QUEUE_NAME,
    actor_name=config.MODELS_TRAINING_QUEUE_NAME,
)
def run_train_model_task(model_id: str, dataset_id: str, model_params: Dict):
    """
    Trains a model and notifies the server when it is finished.
    """
    logger.info(f'Downloading dataset: {dataset_id}')
    dataset_path = files_service.download_dataset(dataset_id)
    model_path = files_service.get_model_local_path(model_id)

    logger.info(f'Training model {model_id}')
    network, network_config, accuracy = train_model(dataset_path, model_params)
    export_model(model_path, network)
    logger.info(f'Finished training model {model_id}')

    files_service.upload_model(model_id)
    logger.info(f'Uploaded model {model_id}')

    network_config['accuracy'] = accuracy
    notify_finished(model_id, network_config)
    logger.info(f'Notified server that model {model_id} is finished')

    files_service.delete_dataset_local_file(dataset_id)
    files_service.delete_model_local_file(model_id)
    logger.info(f'Deleted dataset and model files')

    return None


def train_model(dataset_path: str, params: Dict):
    """
    Trains a model.
    """
    df = files_service.get_dataset_data_frame(dataset_path)
    network_generator = NetworkGenerator(df, params)
    return network_generator.get_best_network()


def notify_finished(model_id: str, network_config: Dict):
    """
    Sends a notification to the server that the model is finished.
    """
    requests.post(config.WEBHOOK_URL.format(model_id=model_id),
                  headers={'x-token': config.WEBHOOK_TOKEN},
                  json=network_config)
