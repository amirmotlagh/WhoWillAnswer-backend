from contextlib import asynccontextmanager
from app.infrastructure.cache.redis_client import redis_client
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis_client.connect()
    except Exception as e:
        ##TODO add logging
        raise RuntimeError(f"Failed to connect to Redis: {e}")


    yield
    await redis_client.disconnect()

app = FastAPI(lifespan=lifespan)

# app.include_router(...)  # Add your routers here
# e.g., app.include_router(user_router)