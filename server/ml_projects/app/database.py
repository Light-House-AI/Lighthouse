"""
Contains the configuration for the database.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config


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


SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=get_engine())


def get_session():
    """
    Returns a session instance.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def check_db_connection(logger: logging.Logger):
    """
    Tests the database connection.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
