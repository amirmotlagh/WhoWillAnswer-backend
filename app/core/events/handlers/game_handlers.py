from typing import Any

from app.infrastructure.cache.game_cache import set_game_players, set_game_state
from app.infrastructure.websocket.broadcaster import broadcast_game_created
from app.logger import get_logger


logger = get_logger("app.core.events.handlers")

async def on_match_created(envelope: dict[str, Any]) -> None:
    game_data = envelope.get("payload", {}).get("game_data")
    if not game_data:
        logger.error("on_match_created received event without game_data: %s", envelope)
        return

    event_id = envelope.get("event_id")
    logger.info("on_match_created processing event_id=%s", event_id)
    
    game_id = game_data.get("id")
    creator_id = game_data.get("creator", {}).get("id")
    state = game_data.get("state", "waiting") # Default to waiting if not in schema
    
    if game_id:
        await set_game_state(game_id, state)
        if creator_id:
            await set_game_players(game_id, [creator_id])
        
        await broadcast_game_created(game_data)
        logger.info(f"Match created successfully processed for game_id: {game_id}")

        #TODO: prepare other necessary data for the game (e.g. questions) and cache it
    else:
        logger.error("on_match_created received event with invalid game_data: %s", game_data)


async def on_match_started(envelope: dict[str, Any]) -> None:
    #TODO: implement match started logic (e.g notify players)
    logger.info("on_match_started received event_id=%s", envelope.get("event_id"))