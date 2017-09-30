import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)


def get_connection():
    conn = redis.Redis(connection_pool=POOL)
    return conn