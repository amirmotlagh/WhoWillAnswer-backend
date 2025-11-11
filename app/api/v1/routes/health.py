import redis
from app.config import settings

r = redis.Redis(host=settings.REDIS_HOST,socket_timeout=1)
def is_redis_available():
    try:
        r.ping()
        ##TODO: add logging
        return True
    except Exception:
        ##TODO add logging
        return False




