from fastapi import WebSocket
from app.logger import get_logger

logger = get_logger('app.websocket.manager')


class WebsocketManager:
	def __init__(self) -> None:
		self.active_users: dict[int, WebSocket] = {}

	async def connect(self, user_id: int, websocket: WebSocket) -> None:
		await websocket.accept()
		previous = self.active_users.get(user_id)
		self.active_users[user_id] = websocket
		if previous is not None and previous is not websocket:
			await previous.close(code=1000)

	async def disconnect(self, user_id: int, websocket: WebSocket | None = None) -> None:
		current = self.active_users.get(user_id)
		if current is None:
			return
		if websocket is not None and current is not websocket:
			return
		del self.active_users[user_id]

	async def send_message(self, user_id: int, message: str):
		ws = self.active_users.get(user_id)
		if not ws:
			return
		try:
			await ws.send_text(message)
		except Exception:
			logger.error('message not sent to user with id: %s', user_id)
			await self.disconnect(user_id)

	async def broadcast(self, message: str):
		for user_id, ws in list(self.active_users.items()):
			try:
				await ws.send_text(message)
			except Exception:
				logger.error('message not sent to user with id: %s', user_id)
				await self.disconnect(user_id)

	async def send_message_to_users(self, user_ids: list[int], message: str):
		for user_id in user_ids:
			await self.send_message(user_id, message)


websocket_manager = WebsocketManager()
