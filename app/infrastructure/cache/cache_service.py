from app.infrastructure.cache.redis_client import redis_client
import json

class CacheService:
    @staticmethod
    async def set(key: str, value: str, expire: int | None = None, serialize: bool = True) -> bool:
        client =await redis_client.get_client()

        try:
            if serialize:
                value = json.dumps(value)
            await client.set(key, value, ex=expire)
            return True
        except Exception:
            # TODO add logging
            return False



    @staticmethod
    async def get(key: str, serialize: bool = True):
        client =await redis_client.get_client()
        try:
            data = await client.get(key)
            if data is None:
                return None

            if serialize:
                return json.loads(data)

            return data
        except Exception:
            # TODO add logging
            return None

    @staticmethod
    async def delete(key: str) -> bool:
        client =await redis_client.get_client()

        try:
            await client.delete(key)
            return True
        except Exception:
            # TODO add logging
            return False
    @staticmethod
    async def exists(key: str) -> bool:
        client = redis_client.get_client()

        try:
            return bool(await client.exists(key))
        except Exception:
            # TODO add logging
            return False