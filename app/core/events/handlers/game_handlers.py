from typing import Any

from app.logger import get_logger


logger = get_logger("app.core.events.handlers")

async def on_match_created(envelope: dict[str, Any]) -> None:
    #TODO: implement match created logic (e.g notify players)
    logger.info("on_match_created received event_id=%s", envelope.get("event_id"))


async def on_match_started(envelope: dict[str, Any]) -> None:
    #TODO: implement match started logic (e.g notify players)
    logger.info("on_match_started received event_id=%s", envelope.get("event_id"))