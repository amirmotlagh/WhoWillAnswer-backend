from app.infrastructure.cache import key_builder
from app.infrastructure.cache.cache_service import CacheService


async def set_room_state(room_id, state):
    key = key_builder.room_state_key(room_id)
    await CacheService.set(key, state)

async def get_room_state(room_id):
    key = key_builder.room_state_key(room_id)
    return await CacheService.get(key)

async  def delete_room_state(room_id):
    key = key_builder.room_state_key(room_id)
    await CacheService.delete(key)

async def set_game_state(game_id,state):
    key = key_builder.game_state_key(game_id)
    await CacheService.set(key, state)

async def get_game_state(game_id):
    key = key_builder.game_state_key(game_id)
    return await CacheService.get(key)

async def delete_game_state(game_id):
    key = key_builder.game_state_key(game_id)
    await CacheService.delete(key)

