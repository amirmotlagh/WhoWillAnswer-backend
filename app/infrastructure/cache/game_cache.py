from app.core.domain.question import QuestionInfo
from app.logger import get_logger
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.cache.key_builder import KeyBuilder

logger = get_logger(__name__)


class GameCache:
	def __init__(self, game_id: int):
		self.game_id = str(game_id)

	async def set_game_state(self, state: str) -> bool:
		key = KeyBuilder.game_state_key(self.game_id)
		ok = await CacheService.set(key, state, 4 * 60 * 60)
		logger.debug(f'Game state cached -> {key}: {state}')
		return ok

	async def set_game_players(self, player_ids: list[int]) -> bool:
		key = KeyBuilder.game_players_key(self.game_id)
		ok = await CacheService.set(key, player_ids, 4 * 60 * 60)
		logger.debug(f'Game players cached -> {key}: {player_ids}')
		return ok

	async def set_game_questions(self, questions: list[QuestionInfo]) -> bool:
		key = KeyBuilder.game_questions_key(self.game_id)
		cache_data = [question.model_dump() for question in questions]
		added = await CacheService.set(key, cache_data, 4 * 60 * 60)
		logger.debug(
			f'Game questions cached for game {self.game_id} -> {key}: {len(cache_data)} questions added'
		)
		return added

	async def get_game_questions(self) -> list[QuestionInfo] | None:
		key = KeyBuilder.game_questions_key(self.game_id)
		cached_data = await CacheService.get(key)
		if cached_data is None:
			logger.debug(f'Game questions not found in cache for game {self.game_id} -> {key}')
			return None
		logger.debug(
			f'Game questions found in cache for game {self.game_id} -> {key}: {len(cached_data)} questions retrieved'
		)
		return [QuestionInfo(**item) for item in cached_data]

	async def set_game_data(self, game_data: dict) -> bool:
		key = KeyBuilder.game_data_key(self.game_id)
		ok = await CacheService.set(key, game_data, 4 * 60 * 60)
		logger.debug(f'Game data cached -> {key}: {game_data}')
		return ok

	async def get_game_state(self) -> str | None:
		key = KeyBuilder.game_state_key(self.game_id)
		return await CacheService.get(key)

	async def get_game_players(self) -> list[int] | None:
		key = KeyBuilder.game_players_key(self.game_id)
		return await CacheService.get(key)

	async def get_game_data(self) -> dict | None:
		key = KeyBuilder.game_data_key(self.game_id)
		return await CacheService.get(key)
