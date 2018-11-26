from redis import Redis
from models.TvShow import TvShow

def save(key, value, number):
    r = Redis(host='localhost', port=6379, db=0)
    r.hset(key, value, number)

def get_all_tv_shows():
    r = Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    tv_shows = []
    
    for key in r.scan_iter():
        name = r.hget(key, 'name')
        episode = r.hget(key, 'last_episode')
        tv_shows.append(TvShow(key, name, episode))

    return tv_shows
