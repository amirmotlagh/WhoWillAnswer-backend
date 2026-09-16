from typing import Any

from app.config import settings
from app.infrastructure.cache.game_cache import GameCache
from app.core.services.question_service import QuestionService
from app.infrastructure.database.repositories.category_repository import CategoryRepository
from app.infrastructure.database.repositories.question_repository import QuestionRepository
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.websocket.broadcaster import (
	broadcast_game_created,
	broadcast_game_questions_prepared,
)
from app.logger import get_logger
from app.utils.enums import GameState


logger = get_logger('app.core.events.handlers')


async def on_match_created(envelope: dict[str, Any]) -> None:
	game_data = envelope.get('payload', {}).get('game_data')
	if not game_data:
		logger.error('on_match_created received event without game_data: %s', envelope)
		return

	event_id = envelope.get('event_id')
	logger.info('on_match_created processing event_id=%s', event_id)

	game_id = game_data.get('id')
	creator_id = game_data.get('creator', {}).get('id')
	state = game_data.get('state', GameState.WAITING)

	if game_id:
		game_cache = GameCache(game_id)
		state_cached = await game_cache.set_game_state(state)
		players_cached = True
		if creator_id:
			players_cached = await game_cache.set_game_players([creator_id])
		if not state_cached or not players_cached:
			logger.error('on_match_created cache write failed for game_id=%s', game_id)
			return
		await broadcast_game_created(game_data)

		question_count = game_data.get('max_players', 10) * settings.QUESTIONS_PER_PLAYER
		async with AsyncSessionLocal() as session:
			try:
				question_repo = QuestionRepository(session)
				category_repo = CategoryRepository(session)
				qs = QuestionService(question_repo, category_repo)
				questions_prepared = await qs.prepare_game_questions(
					game_id, game_data.get('category').get('id'), question_count
				)
				logger.info(f'Match created successfully processed for game_id: {game_id}')
				if not questions_prepared:
					logger.error(f'Failed to prepare questions for game_id: {game_id}')
					return
				await session.commit()
				await broadcast_game_questions_prepared(game_id)
			except Exception:
				await session.rollback()
				logger.error('on_match_created database operation failed', exc_info=True)
				raise
		# TODO: prepare other necessary data for the game (e.g. questions) and cache it
	else:
		logger.error('on_match_created received event with invalid game_data: %s', game_data)


async def on_match_started(envelope: dict[str, Any]) -> None:
	# TODO: implement match started logic (e.g notify players)
	logger.info('on_match_started received event_id=%s', envelope.get('event_id'))
