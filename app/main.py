from contextlib import asynccontextmanager
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.database.session import engine
from fastapi import FastAPI
from app.logger import setup_logging, get_logger
from app.api.v1.routes.health import health_router
import asyncio
from sqlalchemy import text

async def wait_for_db(retries=5, delay=2):
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return
        except Exception:
            if i == retries - 1:
                raise
            await asyncio.sleep(delay)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = get_logger("app")
    logger.info("Application startup: Logging configured")
    try:
        await redis_client.connect()
    except Exception as e:
        logger.exception("Failed to connect to Redis")
        raise RuntimeError("Failed to connect to Redis") from e
    
    redis_connected = await redis_client.health_check()
    if not redis_connected:
        raise RuntimeError("Redis health check failed")

    # Verify DB connection and basic health
    await wait_for_db()
    logger.info("Application startup: App resources initialized")
    
    yield
    await redis_client.disconnect()

app = FastAPI(lifespan=lifespan)

# app.include_router(...)  # Add your routers here
app.include_router(health_router)