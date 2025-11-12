from app.infrastructure.cache.redis_client import redis_client

class CacheService:
    @staticmethod
    async def set(key: str, value: str, expire: int | None = None):
        client = redis_client.get_client()
        await client.set(key, value, ex=expire)

    @staticmethod
    async def get(key: str):
        client = redis_client.get_client()
        return await client.get(key)

    @staticmethod
    async def delete(key: str):
        client = redis_client.get_client()
        await client.delete(key)

    @staticmethod
    async def exists(key: str):
        client = redis_client.get_client()
        return await client.exists(key)