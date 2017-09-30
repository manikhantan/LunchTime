import pymongo
from pymongo import MongoClient

from projects.restApi.utils.config_util import get_config

conn = None


def mongodb():
    if conn:
        return conn
    config = get_config()
    mongo_uri = config['DATA']['MONGO_URI']
    db_name = mongo_uri.split('/')[3]
    client = MongoClient(mongo_uri)
    return client[db_name]
