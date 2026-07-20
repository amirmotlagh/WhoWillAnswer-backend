from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.cache.key_builder import KeyBuilder
from app.logger import get_logger
from app.core.domain.category import CategoryInfo
from typing import Any


logger = get_logger(__name__)


async def get_category_cache() -> list[CategoryInfo] | None:
	key = KeyBuilder.all_categories_cache_key()
	cached_data: list[dict[str, Any]] | None = await CacheService.get(key)
	if cached_data is None:
		return None
	return [CategoryInfo(**item) for item in cached_data]


async def set_category_cache(categories: list[CategoryInfo]) -> bool:
	key = KeyBuilder.all_categories_cache_key()
	cache_data = [category.model_dump() for category in categories]

	return await CacheService.set(key, cache_data, expire=60 * 60 * 24)


async def delete_category_cache() -> bool:
	key = KeyBuilder.all_categories_cache_key()
	return await CacheService.delete(key)
