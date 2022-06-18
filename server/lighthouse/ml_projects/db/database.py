"""Contains the configuration for the database."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from lighthouse.config import config
from lighthouse.logger import logger


def get_engine():
    """
    Returns an engine instance.
    """
    connection_uri = config.SQLALCHEMY_DATABASE_URI

    # fix the url for postgresql
    if connection_uri.startswith("postgres://"):
        connection_uri = connection_uri.replace("postgres://", "postgresql://",
                                                1)

    log_queries = config.DEBUG
    engine = create_engine(connection_uri, echo=log_queries)
    return engine


def get_session_factory(engine: Engine):
    """
    Returns a session factory instance.
    """
    session_factory = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

    return session_factory


def check_db_connection(db: Session):
    """
    Tests the database connection.
    """
    try:
        db.execute("SELECT 1")
        logger.info("Database connection successful!")
    except Exception as e:
        logger.error(e)
        raise e
