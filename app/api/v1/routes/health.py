from starlette.responses import JSONResponse
from app.config import settings
from app.infrastructure.cache.redis_client import redis_client

async def is_redis_available():
    try:
        await redis_client.health_check()
        ##TODO: add logging
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception:
        ##TODO add logging
        return JSONResponse(status_code=503, content={"status": "error"})




