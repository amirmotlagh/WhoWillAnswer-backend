import json
import uuid

from datetime import datetime, timezone
from typing import Any

from nats.aio.client import Client as NATSClient
from nats.errors import TimeoutError as NatsTimeoutError
from nats.js import JetStreamContext
from nats.js.errors import NoStreamResponseError
from app.logger import get_logger

logger = get_logger('app.messaging.publisher')

_DEFAULT_TIMEOUT = 5.0  # seconds


class EventPublisher:
	def __init__(self, js: JetStreamContext, nc: NATSClient) -> None:
		self._js = js
		self._nc = nc

	@staticmethod
	def _build_envelope(subject: str, payload: dict[str, Any], event_id: str) -> dict[str, Any]:
		return {
			'event_id': event_id,
			'subject': subject,
			'timestamp': datetime.now(timezone.utc).isoformat(),
			'payload': payload,
		}

	async def publish(
		self,
		subject: str,
		payload: dict[str, Any],
		event_id: str | None = None,
		timeout: float = _DEFAULT_TIMEOUT,
	) -> str:
		event_id = event_id or str(uuid.uuid4())
		envelope = self._build_envelope(subject=subject, payload=payload, event_id=event_id)
		data = json.dumps(envelope).encode()

		headers = {'Nats-Msg-Id': event_id}

		try:
			ack = await self._js.publish(
				subject=subject, payload=data, headers=headers, timeout=timeout
			)
			logger.debug(
				"Published event '%s' to '%s' (seq=%s, duplicate=%s)",
				event_id,
				subject,
				ack.seq,
				ack.duplicate,
			)
		except NoStreamResponseError:
			logger.error(
				"No stream found for subject '%s'. Event '%s' was NOT persisted.",
				subject,
				event_id,
			)
			raise
		return event_id

	async def request(
		self, subject: str, payload: dict[str, Any], timeout: float = _DEFAULT_TIMEOUT
	) -> dict[str, Any]:
		data = json.dumps(payload).encode()

		try:
			response = await self._nc.request(subject=subject, payload=data, timeout=timeout)
			return json.loads(response.data.decode())
		except NatsTimeoutError:
			logger.error(
				"Request to '%s' timed out after %s seconds. Payload: %s",
				subject,
				timeout,
				payload,
			)
			raise
		except json.JSONDecodeError as e:
			logger.error("Failed to decode JSON response from '%s': %s", subject, e)
		except Exception as e:
			logger.error("Error during request to '%s': %s", subject, e)
			raise
		return {}
