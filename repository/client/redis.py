from redis import Redis

def save(key, value, number):
    r = Redis(host='localhost', port=6379, db=0)
    r.hset(key, value, number)
