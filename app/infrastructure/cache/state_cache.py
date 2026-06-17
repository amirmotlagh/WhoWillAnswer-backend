from app.infrastructure.cache.key_builder import KeyBuilder
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.database.models import GameState


async def set_room_state(room_id: str, state: GameState):
	key = KeyBuilder.room_state_key(room_id)
	await CacheService.set(key, state)


async def get_room_state(room_id):
	key = KeyBuilder.room_state_key(room_id)
	return await CacheService.get(key)


async def delete_room_state(room_id):
	key = KeyBuilder.room_state_key(room_id)
	await CacheService.delete(key)


async def set_game_state(game_id, state):
	key = KeyBuilder.game_state_key(game_id)
	await CacheService.set(key, state)


async def get_game_state(game_id):
	key = KeyBuilder.game_state_key(game_id)
	return await CacheService.get(key)


async def delete_game_state(game_id):
	key = KeyBuilder.game_state_key(game_id)
	await CacheService.delete(key)


async def set_game_players(game_id: str, players: list[int]):
	key = KeyBuilder.game_players_key(game_id)
	await CacheService.set(key, players)


async def get_game_players(game_id: str):
	key = KeyBuilder.game_players_key(game_id)
	return await CacheService.get(key)
