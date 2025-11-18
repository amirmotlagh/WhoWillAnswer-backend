from contextlib import asynccontextmanager
from app.infrastructure.cache.redis_client import redis_client
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Add your startup logic here

    # For example, you might want to connect to a database
    # db.connect()
    # Or initialize some resources
    # resource.initialize()
    yield
    # TODO: Add your shutdown logic here
    # For example, you might want to disconnect from a database
    # db.disconnect()
    # Or release some resources
    # resource.release()

app = FastAPI(lifespan=lifespan)

# app.include_router(...)  # Add your routers here
# e.g., app.include_router(user_router)