from redis import Redis
from models.TvShow import TvShow

host = config('REDIS_HOST')
port = config('REDIS_PORT')
db = config('REDIS_DB', cast=int)

def save(key, value, number):
    r = Redis(host=host, port=port, db=db)
    r.hset(key, value, number)

def get_all_tv_shows():
    r = Redis(host=host, port=port, db=db)
    tv_shows = []

    for key in r.scan_iter():
        name = r.hget(key, 'name')
        episode = r.hget(key, 'last_episode')
        tv_shows.append(TvShow(key, name, episode))

    return tv_shows
