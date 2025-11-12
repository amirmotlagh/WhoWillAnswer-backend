import redis
from starlette.responses import JSONResponse

from app.config import settings

r = redis.Redis(host=settings.REDIS_HOST,socket_timeout=1)
def is_redis_available():
    try:
        r.ping()
        ##TODO: add logging
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception:
        ##TODO add logging
        return JSONResponse(status_code=503, content={"status": "error"})




