from fastapi import FastAPI

from lighthouse.logger import logger
from lighthouse.ml_projects.db.database import (get_session_factory,
                                                get_engine,
                                                check_db_connection)

from lighthouse.mlops.monitoring.db import connect_to_mongo


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

    mongo_client = connect_to_mongo()
    app.state.mongo_client = mongo_client

    logger.info("MongoDB connection successful!")
    return True


def _shutdown_mongo(app: FastAPI):
    """
    Disposes the MongoDB connection.
    """

    app.state.mongo_client.close()
    logger.info("MongoDB connection closed.")
    return True


def startup(app: FastAPI):
    """
    Actions to run on application startup.
    """

    async def _startup():
        # setup database
        _setup_db(app)
        check_db_connection(app.state.db_session_factory, logger)

        # setup mongo
        _setup_mongo(app)

    return _startup


def shutdown(app: FastAPI):
    """
    Actions to run on application's shutdown.
    """

    async def _shutdown():
        _shutdown_db(app)
        _shutdown_mongo(app)

    return _shutdown
