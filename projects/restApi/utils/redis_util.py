import redis

from projects.restApi.utils.config_util import get_config

configs = get_config()
redis_uri = configs['DATA']['REDIS_HOST']
host, port = redis_uri.split(':')
POOL = redis.ConnectionPool(host=host, port=port, db=0)


def get_connection():
    conn = redis.Redis(connection_pool=POOL)
    return conn
