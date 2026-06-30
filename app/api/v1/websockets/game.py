import asyncio
import json

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import ValidationError
from starlette.websockets import WebSocketState

from app.infrastructure.websocket.connection_manager import websocket_manager
from app.logger import get_logger
from app.schemas.websocket import IncomingWSMessage
from app.utils.jwt import decode_token

logger = get_logger('app.websocket.game')

game_ws_router = APIRouter(prefix='/ws', tags=['websockets'])
AUTH_MESSAGE_TIMEOUT_SECONDS = 20
INACTIVITY_TIMEOUT_SECONDS = 60


@game_ws_router.websocket('/')
async def game_websocket_endpoint(ws: WebSocket):
	await ws.accept()
	user_id: int | None = None

	try:
		auth_message = await asyncio.wait_for(
			ws.receive_json(), timeout=AUTH_MESSAGE_TIMEOUT_SECONDS
		)
	except asyncio.TimeoutError:
		await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason='Auth message timeout')
		return

	if not isinstance(auth_message, dict):
		await ws.close(
			code=status.WS_1008_POLICY_VIOLATION, reason='Invalid authentication message format'
		)
		return

	try:
		token = auth_message.get('token')
		if not token or not isinstance(token, str):
			await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason='Auth token not provided')
			return

		token_data = await decode_token(token)
		user_id = token_data.user_id
		await websocket_manager.connect(user_id, ws)
		await ws.send_json({'status': 'authenticated'})

		while True:
			try:
				message = await asyncio.wait_for(
					ws.receive_text(), timeout=INACTIVITY_TIMEOUT_SECONDS
				)
			except asyncio.TimeoutError:
				logger.info('Disconnecting user %s due to inactivity.', user_id)
				await ws.close(code=status.WS_1000_NORMAL_CLOSURE, reason='Inactivity timeout')
				break

			try:
				parsed_msg = IncomingWSMessage.model_validate_json(message)
				if user_id is None:
					logger.error(
						'process_message called with user_id=None, this should not happen.'
					)
					break
				await process_message(parsed_msg, user_id)
			except (ValidationError, json.JSONDecodeError) as e:
				error_payload = {'error': 'Invalid message format', 'details': str(e)}
				await websocket_manager.send_message(user_id, json.dumps(error_payload))
				continue
	except WebSocketDisconnect as e:
		logger.info('Connection aborted for user %s: %s', user_id, str(e))
	except HTTPException as e:
		reason = e.detail if isinstance(e.detail, str) else 'Authentication failed'
		await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason=reason)
	except Exception as e:
		logger.error('Unexpected error in websocket for user %s: %s', user_id, str(e))
		if ws.client_state != WebSocketState.DISCONNECTED:
			await ws.close(
				code=status.WS_1011_INTERNAL_ERROR, reason='An unexpected server error occurred.'
			)
	finally:
		if user_id is not None:
			logger.info('Cleaning up connection for user %s', user_id)
			await websocket_manager.disconnect(user_id, ws)


async def process_message(parsed_msg: IncomingWSMessage, user_id: int):
	match parsed_msg.type:
		# TODO: Implement actual game logic handlers
		# e.g., case 'join_game': await handle_join_game(user_id, parsed_msg.data)
		# e.g., case 'submit_answer': await handle_submit_answer(user_id, parsed_msg.data)
		case 'ping':
			await websocket_manager.send_message(user_id, 'pong')
		case 'message':
			if parsed_msg.receiver_id is not None:
				await websocket_manager.send_message(
					parsed_msg.receiver_id, f'Message received: {parsed_msg.data}'
				)
		case 'broadcast':
			await websocket_manager.broadcast(f'Message received: {parsed_msg.data}')
		case _:
			await websocket_manager.send_message(
				user_id, f'Message received: {parsed_msg.model_dump()}'
			)
