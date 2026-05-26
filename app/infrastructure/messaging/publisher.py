import json
import uuid

from datetime import datetime
from typing import Any

from nats.js import JetStreamContext
from nats.js.errors import NoStreamResponseError
from app.logger import get_logger


logger = get_logger("app.messaging.publisher")

_DEFAULT_TIMEOUT = 5.0 # seconds

class EventPublisher:

    def __init__(self, js: JetStreamContext) -> None:
        self._js = js

    @staticmethod
    def _build_envelope(subject: str, payload: dict[str, Any], event_id: str) -> dict[str, Any]:
        return {
            "event_id": event_id,
            "subject": subject,
            "timestamp":datetime.now().isoformat(),
            "payload": payload
        }

    async def publish(
            self,
            subject: str,
            payload: dict[str, Any],
            event_id: str | None = None,
            timeout: float = _DEFAULT_TIMEOUT
            ) -> str:
        
        event_id = event_id or str(uuid.uuid4())
        envelope = self._build_envelope(subject=subject, payload=payload, event_id=event_id)
        data = json.dumps(envelope).encode()

        headers = {"Nats-Msg-Id": event_id}

        try:
            ack = await self._js.publish(
                subject=subject,
                payload=data,
                headers=headers,
                timeout=timeout
            )
            logger.debug(
                "Published event '%s' to '%s' (seq=%s, duplicate=%s)",
                event_id, subject, ack.seq, ack.duplicate,
            )
        except NoStreamResponseError:
            logger.error(
                "No stream found for subject '%s'. Event '%s' was NOT persisted.",
                subject, event_id,
            )
            raise
        return event_id
        
    async def request(
            self,
            subject: str,
            payload: dict[str, Any],
            timeout: float = _DEFAULT_TIMEOUT
            ) -> dict[str, Any]:
        
        data = json.dumps(payload).encode()

        response = await self._js._nc.request(subject=subject, payload=data, timeout=timeout)
        return json.loads(response.data.decode())