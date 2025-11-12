import redis.asyncio as redis
from app.config import  settings


pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    max_connections=settings.REDIS_MAX_CONNECTIONS
)

redis_client = redis.Redis(connection_pool=pool)