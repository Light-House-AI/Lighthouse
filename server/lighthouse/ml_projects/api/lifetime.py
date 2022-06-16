from fastapi import FastAPI

from lighthouse.config import config
from lighthouse.logger import logger
from lighthouse.ml_projects.mongo import connect_to_mongo
from lighthouse.ml_projects.services.dataset_file import create_directories
from lighthouse.ml_projects.services.dramatiq import init_dramatiq
from lighthouse.ml_projects.db.database import (
    get_session_factory,
    get_engine,
    check_db_connection,
)


def startup(app: FastAPI):
    """
    Actions to run on application startup.
    """
    async def _startup():
        # create directories
        create_directories()

        # setup database
        _setup_db(app)
        check_db_connection(app.state.db_session_factory, logger)

        # setup mongo
        _setup_mongo(app)

        # init dramatiq
        init_dramatiq()

    return _startup


def shutdown(app: FastAPI):
    """
    Actions to run on application's shutdown.
    """
    async def _shutdown():
        _shutdown_db(app)
        _shutdown_mongo(app)

    return _shutdown


def _setup_db(app: FastAPI):
    """
    Creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.
    """

    engine = get_engine()
    session_factory = get_session_factory(engine)

    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    return True


def _shutdown_db(app: FastAPI):
    """
    Disposes the database connection.
    """

    app.state.db_engine.dispose()
    logger.info("Database connection disposed.")
    return True


def _setup_mongo(app: FastAPI):
    """
    Creates a connection to the MongoDB database.
    """

    # Monitors MongoDB connection.
    monitoring_mongo_client = connect_to_mongo(
        config.MONITORING_MONGO_URI,
        config.MONITORING_MONGO_ALIAS,
    )

    app.state.monitoring_mongo_client = monitoring_mongo_client
    logger.info("ML-Monitoring MongoDB connection successful!")

    # ML-Projects MongoDB connection.
    ml_projects_mongo_client = connect_to_mongo(
        config.ML_PROJECTS_MONGO_URI,
        config.ML_PROJECTS_MONGO_ALIAS,
    )

    app.state.ml_projects_mongo_client = ml_projects_mongo_client
    logger.info("ML-Projects MongoDB connection successful!")

    return True


def _shutdown_mongo(app: FastAPI):
    """
    Disposes the MongoDB connection.
    """

    app.state.monitoring_mongo_client.close()
    logger.info("ML-Monitoring MongoDB connection closed.")

    app.state.ml_projects_mongo_client.close()
    logger.info("ML-Projects MongoDB connection closed.")

    return True
