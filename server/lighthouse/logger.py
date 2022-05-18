"""
Contains the Logger class.
"""

import coloredlogs, logging
from .config import config

logger = logging.getLogger(__name__)
coloredlogs.install(level=config.LOG_LEVEL,
                    logger=logger,
                    fmt=config.LOG_FORMAT)
