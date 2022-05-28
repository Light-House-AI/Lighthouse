from fastapi import FastAPI
from lighthouse.ml_projects.db.database import get_session_factory, get_engine, check_db_connection
from lighthouse.logger import logger


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
    return True


def startup(app: FastAPI):
    """
    Actions to run on application startup.
    """

    async def _startup():
        _setup_db(app)
        check_db_connection(app.state.db_session_factory, logger)

    return _startup


def shutdown(app: FastAPI):
    """
    Actions to run on application's shutdown.
    """

    async def _shutdown():
        _shutdown_db(app)

    return _shutdown
