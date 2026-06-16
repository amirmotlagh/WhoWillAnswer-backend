from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.infrastructure.websocket.connection_manager import websocket_manager
from app.logger import get_logger
from app.schemas.websocket import IncomingWSMessage

logger = get_logger("app.websocket.game")


game_ws_router = APIRouter(prefix="/ws", tags=["game"])

@game_ws_router.websocket("/{user_id}")
async def game_websocket_endpoint(ws: WebSocket, user_id: int): #TODO: this should get uset data from request. just for test
    await websocket_manager.connect(user_id, ws)
    try:
        while True:
            message = await ws.receive_text()
            try:
                parsed_msg = IncomingWSMessage.model_validate_json(message)
                await process_message(parsed_msg, user_id)
            except ValidationError:
                await websocket_manager.send_message(user_id, "Invalid message schema or JSON format")
                continue
    except WebSocketDisconnect as e:
         logger.info("Connection aborted for user %s: %s", user_id, str(e))
    except Exception as e:
        logger.error("Unexpected error in websocket for user %s: %s", user_id, str(e))
    finally:
        logger.info("Cleaning up connection for user %s", user_id)
        await websocket_manager.disconnect(user_id, ws)


async def process_message(parsed_msg: IncomingWSMessage, user_id: int):
    match parsed_msg.type:
        case "ping":
            await websocket_manager.send_message(user_id, "pong")
        case "message":
                if parsed_msg.receiver_id is not None:
                    await websocket_manager.send_message(
                        parsed_msg.receiver_id, f"Message received: {parsed_msg.data}"
                    )
        case "broadcast":
            await websocket_manager.broadcast(f"Message received: {parsed_msg.data}")
        case _:
                await websocket_manager.send_message(user_id, f"Message received: {parsed_msg.model_dump()}")