from typing import Any

from app.infrastructure.cache.category_cache import (
	delete_category_cache,
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

	await delete_category_cache()
