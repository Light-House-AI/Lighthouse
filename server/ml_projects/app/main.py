"""
Contains the application startup code.
"""

import logging
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from database import check_db_connection

from logger import logger

# used to retry the app initialization
MAX_TRIES_SECONDS = 30
WAIT_TIME_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_TRIES_SECONDS),
    wait=wait_fixed(WAIT_TIME_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_app(logger: logging.Logger):
    """
    Initializes the application.
    """
    check_db_connection(logger)


def main():
    logger.info("Initializing service")
    init_app(logger)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()