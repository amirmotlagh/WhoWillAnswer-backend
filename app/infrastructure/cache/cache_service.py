from typing import Any

from app.infrastructure.cache.redis_client import redis_client
import json

from app.logger import get_logger

logger = get_logger(__name__)


class CacheService:
	@staticmethod
	async def set(key: str, value: Any, expire: int | None = None, serialize: bool = True) -> bool:
		client = await redis_client.get_client()
		if not client:
			return False

		try:
			if serialize:
				value = json.dumps(value)
			await client.set(key, value, ex=expire)
			return True
		except Exception as e:
			logger.error('Failed to set cache for key: %s. Exception: %s', key, e)
			return False

	@staticmethod
	async def get(key: str, serialize: bool = True):
		client = await redis_client.get_client()
		if not client:
			return None

		try:
			data = await client.get(key)
			if data is None:
				return None

			if serialize:
				return json.loads(data)

			return data
		except Exception as e:
			logger.error('Failed to get cache for key: %s. Exception: %s', key, e)
			return None

	@staticmethod
	async def delete(key: str) -> bool:
		client = await redis_client.get_client()
		if not client:
			return False

		try:
			await client.delete(key)
			return True
		except Exception as e:
			logger.error('Failed to delete cache for key: %s. Exception: %s', key, e)
			return False

	@staticmethod
	async def exists(key: str) -> bool:
		client = await redis_client.get_client()
		if not client:
			return False

		try:
			return bool(await client.exists(key))
		except Exception as e:
			logger.error('Failed to get cache for key: %s. Exception: %s', key, e)
			return False
