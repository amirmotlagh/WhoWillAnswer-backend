from contextlib import asynccontextmanager
from app.infrastructure.cache.redis_client import redis_client
from fastapi import FastAPI
from app.logger import setup_logging, get_logger
from app.api.v1.routes.health import health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = get_logger("app")
    logger.info("Application startup: Logging configured")
    try:
        await redis_client.connect()
    except Exception as e:
        logger.exception(f"Failed to connect to Redis: {e}")
        raise RuntimeError(f"Failed to connect to Redis: {e}") from e
    
    redis_connected = await redis_client.health_check()
    if not redis_connected:
        raise RuntimeError("Redis health check failed")

    logger.info("Application startup: App resources initialized")
    
    yield
    await redis_client.disconnect()

app = FastAPI(lifespan=lifespan)

# app.include_router(...)  # Add your routers here
app.include_router(health_router)