from typing import Any

from app.core.domain.category import CategoryInfo
from app.infrastructure.cache.category_cache import (
	delete_category_cache,
	get_category_cache,
	set_category_cache,
)
from app.logger import get_logger


logger = get_logger(__name__)


async def on_category_created(envelope: dict[str, Any]) -> None:
	category_data = envelope.get('payload', {}).get('category_data')
	if not category_data:
		logger.error('on_category_created received event without category_data: %s', envelope)
		return
	event_id = envelope.get('event_id')
	logger.info('on_category_created processing event_id=%s', event_id)

	categories = await get_category_cache()
	if not categories:
		return
	categories.append(CategoryInfo(**category_data))
	ok = await set_category_cache(categories)
	if not ok:
		logger.error(
			'on_category_created cache write failed for category_id=%s', category_data['id']
		)
		await delete_category_cache()
		return
	logger.info(f'Category created successfully processed for category_id: {category_data["id"]}')
