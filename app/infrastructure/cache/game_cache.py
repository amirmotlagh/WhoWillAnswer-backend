import json
from app.logger import get_logger
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.cache.key_builder import KeyBuilder

logger = get_logger(__name__)

async def set_game_state(game_id: int, state: str) -> None:
    key = KeyBuilder.game_state_key(str(game_id))
    await CacheService.set(key, state)
    logger.debug(f"Game state cached -> {key}: {state}")

async def set_game_players(game_id: int, player_ids: list[int]) -> None:
    key = KeyBuilder.game_players_key(str(game_id))
    await CacheService.set(key, json.dumps(player_ids))
    logger.debug(f"Game players cached -> {key}: {player_ids}")

async def get_game_state(game_id: int) -> str | None:
    key = KeyBuilder.game_state_key(str(game_id))
    return await CacheService.get(key)

async def get_game_players(game_id: int) -> list[int] | None:
    key = KeyBuilder.game_players_key(str(game_id))
    return await CacheService.get(key)