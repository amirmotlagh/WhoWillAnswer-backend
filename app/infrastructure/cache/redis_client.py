import redis.asyncio as redis
from app.config import settings


class RedisClient:

    def __init__(self):
        self._pool = None
        self._client = None

    async def connect(self):
        if not self._pool:
            self._pool =  redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS
            )
        self._client = redis.Redis(connection_pool=self._pool)
        # TODO: add logging

    async def disconnect(self):
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
            self._client = None
            # TODO: add logging

    def get_client(self):
        if not self._client:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._client

    async def health_check(self):
        try:
            await self._client.ping()
            return True
        except Exception:
            return False


redis_client = RedisClient()