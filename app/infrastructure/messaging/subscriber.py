import json
from collections.abc import Awaitable, Callable
from typing import Any

from nats.aio.msg import Msg
from nats.js import JetStreamContext
from nats.js.api import AckPolicy, ConsumerConfig, DeliverPolicy
from app.logger import get_logger


logger = get_logger("app.messaging.subscriber")

Handler = Callable[[dict[str, Any]], Awaitable[None]]

_DEFAULT_ACK_WAIT = 30 # seconds
_DEFAULT_MAX_DELIVER = 5

class EventSubscriber:
    def __init__(self, js: JetStreamContext):
        self._js = js
        self._subscriptions: list = []

    async def subscribe(
            self,
            subject: str,
            handler: Handler,
            durable: str,
            queue: str | None = None,
            ack_wait: int = _DEFAULT_ACK_WAIT,
            max_deliver: int = _DEFAULT_MAX_DELIVER,
    ) -> None:
            config = ConsumerConfig(
                durable_name=durable,
                deliver_policy=DeliverPolicy.ALL,
                ack_policy=AckPolicy.EXPLICIT,
                ack_wait=ack_wait,
                max_deliver=max_deliver,
                filter_subject=subject,
            )

            sub = await self._js.subscribe(
                 subject=subject,
                 durable=durable,
                 queue=queue,
                 config=config,
                 cb=self._make_wrapper(handler, subject),
                 manual_ack=True
            )

            self._subscriptions.append(sub)
            logger.info(
                "subscribed to '%s' (durable='%s', queue='%s')", subject, durable, queue or "none",
            )

    async def unsubscribe_all(self) -> None:
        for sub in self._subscriptions:
            try:
                await sub.unsubscribe()
            except Exception as exc:
                logger.warning("Error unsubscribing: %s", exc)
        self._subscriptions.clear()
        logger.info("All NATS subscriptions removed.")
    

    @staticmethod
    def _make_wrapper(handler: Handler, subject: str) -> Callable[[Msg], Awaitable[None]]:
        async def _wrapper(msg: Msg) -> None:
            try:
                envelope = json.loads(msg.data.decode())
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                logger.error(
                    "Unparseable message on '%s' — terminating (no redelivery). Error: %s",
                    subject,
                    exc,
                )
                await msg.term()
                return

            event_id = envelope.get("event_id", "unknown")

            try:
                await handler(envelope)
                await msg.ack()
                logger.debug("Acked event '%s' on '%s'.", event_id, subject)
            except Exception as exc:
                logger.exception(
                    "Handler failed for event '%s' on '%s' — naking for redelivery. Error: %s",
                    event_id,
                    subject,
                    exc,
                )
                await msg.nak()

        return _wrapper