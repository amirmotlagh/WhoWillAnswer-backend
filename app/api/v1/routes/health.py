import redis
from app.config import settings

r=redis.Redis(host=settings.REDIS_HOST,socket_timeout=1)
def is_redis_available():
    try:
        r.ping()
        #print("Redis is healthy")
        return True
    except Exception:
        #print("Redis is not available")
        return False



