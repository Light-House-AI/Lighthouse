from mongoengine import connect, MongoClient
from lighthouse.config import config

def connect_to_mongo(db_host :str = config.MONGO_URI) -> MongoClient:
    """
    Connect to the specified database.
    """
    return connect(host=db_host)
    

