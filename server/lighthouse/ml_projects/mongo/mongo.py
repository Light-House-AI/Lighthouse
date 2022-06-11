"""MongoDB connection."""

from mongoengine import connect
from lighthouse.config import config


def connect_to_mongo(db_host: str, alias: str = "default"):
    """
    Connect to the specified database.
    """
    return connect(host=db_host, alias=alias)
