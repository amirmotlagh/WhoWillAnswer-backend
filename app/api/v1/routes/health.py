from starlette.responses import JSONResponse
from app.infrastructure.cache.redis_client import redis_client
from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])

@health_router.get("/", summary="Check application health")
async def check_app_health():
    # Example health check logic
    return JSONResponse(status_code=200, content={"status": "ok"})

@health_router.get("/redis", summary="Check Redis health")
async def is_redis_available():
    try:
        ok_state = await redis_client.health_check()
        if not ok_state:
            return JSONResponse(status_code=503, content={"status": "error"})
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception:
        ##TODO add logging
        return JSONResponse(status_code=503, content={"status": "error"})




