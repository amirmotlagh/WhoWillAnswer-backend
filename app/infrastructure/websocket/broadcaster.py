import json
from typing import Any
from app.infrastructure.websocket.connection_manager import websocket_manager
from app.logger import get_logger

logger = get_logger(__name__)


async def broadcast_game_created(game_data: dict[str, Any]) -> None:
	"""Broadcasts the game.created event to all connected WebSocket clients."""
	try:
		message = {'type': 'game.created', 'payload': game_data}
		await websocket_manager.broadcast(json.dumps(message))
		logger.debug(f'Broadcasted game.created for game_id: {game_data.get("id")}')
	except Exception as e:
		logger.error(f'Failed to broadcast game.created event: {e}')
		raise
