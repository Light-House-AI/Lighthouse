"""MongoDB connection."""

from mongoengine import connect


def connect_to_mongo(db_host: str, alias: str = "default"):
    """
    Connect to the specified database.
    """
    return connect(host=db_host, alias=alias, uuidRepresentation="standard")
