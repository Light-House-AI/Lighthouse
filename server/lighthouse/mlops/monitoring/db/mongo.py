from mongoengine import connect
from lighthouse.config import config

def connect_to_mongo(db_host :str = config.MONGO_URI):
    """
    Connect to the specified database.
    """
    return connect(host=db_host)
    

