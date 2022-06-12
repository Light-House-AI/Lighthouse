"""Dramatiq task execution service"""

import dramatiq
from lighthouse.config import config
from lighthouse.logger import logger
from dramatiq.brokers.redis import RedisBroker


def init_dramatiq():
    """Initialize Dramatiq task execution service."""
    redis_broker = RedisBroker(url=config.DRAMATIQ_REDIS_BROKER_URL)
    dramatiq.set_broker(redis_broker)
    logger.info(f'Initialized Dramatiq task execution service')
