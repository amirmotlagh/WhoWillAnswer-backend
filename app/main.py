from contextlib import asynccontextmanager
import logging

from app.core.events.subscriptions import register_subscribers
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.database.session import engine
from fastapi import FastAPI
from app.infrastructure.messaging import subjects
from app.infrastructure.messaging.publisher import EventPublisher
from app.infrastructure.messaging.subscriber import EventSubscriber
from app.logger import setup_logging, get_logger
from app.api.v1.routes.health import health_router
import asyncio
from sqlalchemy import text
from app.infrastructure.messaging.nats_client import NATSClientManager

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

async def wait_for_redis(logger: logging.Logger):
    try:
        await redis_client.connect()
        logger.info("Redis connection is Ready.")
    except Exception as e:
        logger.exception("Failed to connect to Redis")
        raise RuntimeError("Failed to connect to Redis") from e
    
    redis_connected = await redis_client.health_check()
    if not redis_connected:
        raise RuntimeError("Redis health check failed")

async def wait_for_nats(app: FastAPI, logger: logging.Logger) -> NATSClientManager:
    try:
        nats_manager = NATSClientManager()
        await nats_manager.connect()
        logger.info("NATS JetStream Ready.")
        nats_state = await nats_manager.health_check()
        if nats_state.get("status") != "connected":
            raise RuntimeError("NATS health check failed")
        app.state.nats = nats_manager
        app.state.publisher = EventPublisher(js=nats_manager.jetstream, nc=nats_manager.client)
        app.state.subscriber = EventSubscriber(nc=nats_manager.client ,js=nats_manager.jetstream)
        return nats_manager
    except Exception as e:
        logger.exception("Failed to connect to NATS")
        raise RuntimeError("Failed to connect to NATS") from e

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = get_logger("app")
    logger.info("Application startup: Logging configured")
    
    await wait_for_db()
    await wait_for_redis(logger=logger)
    nats_manager = await wait_for_nats(app=app, logger=logger)
    
    await register_subscribers(app)
    logger.info("Event subscribers registered.")
    
    logger.info("Application startup: App resources initialized")
    
    yield
    logger.info("shutting down...")

    await app.state.subscriber.unsubscribe_all()

    await nats_manager.drain()
    await nats_manager.close()
    logger.info("NATS disconnected.")

    await redis_client.disconnect()
    logger.info("Redis disconnected.")

app = FastAPI(lifespan=lifespan)

# app.include_router(...)  # Add your routers here
app.include_router(health_router)