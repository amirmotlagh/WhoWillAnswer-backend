from app.infrastructure.cache.redis_client import redis_client

class CacheService:
    @staticmethod
    async def set(key: str, value: str, expire: int | None = None):
        await redis_client.set(key, value, ex=expire)

    @staticmethod
    async def get(key: str):
        return await redis_client.get(key)

    @staticmethod
    async def delete(key: str):
        await redis_client.delete(key)

    @staticmethod
    async def exists(key: str):
        return await redis_client.exists(key)