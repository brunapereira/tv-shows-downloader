from redis import Redis
from prettyconf import config

host = config('REDIS_HOST')
port = config('REDIS_PORT')
db = config('REDIS_DB', cast=int)


def save(key, value, number):
    r = Redis(host=host, port=port, db=db)
    r.hset(key, value, number)
