import nats
from nats.aio.client import Client as NATSClient
from nats.js import JetStreamContext
from nats.js.api import (
    RetentionPolicy,
    StorageType,
    StreamConfig,
)
from nats.js.errors import NotFoundError

from app.config import settings
from app.logger import get_logger


logger = get_logger("app.messaging.nats_client")

_STREAM_NAME = "GAME"
_STREAM_SUBJECTS = ["game.>"]
_DUPLICATE_WINDOW = 2 * 60
_MAX_AGE = 7 * 24 * 60 * 60
_MAX_MSGS = 1_000_000
_MAX_BYTES = 512 * 1024 * 1024  # 512 MB
_NUM_REPLICAS = 1

class NATSClientManager:

    def __init__(self) -> None:
        self._nc: NATSClient | None = None
        self._js: JetStreamContext | None = None

    @property
    def client(self) -> NATSClient:
        if self._nc is None:
            raise RuntimeError("NATS Client is not connected")
        return self._nc
    
    @property
    def jetstream(self) -> JetStreamContext:
        if self._js is None:
            raise RuntimeError("JetStream context is not initialized")
        return self._js
    
    async def connect(self) -> None:
        logger.info("Connecting to NATS at %s", settings.NATS_URL)

        self._nc = await nats.connect(
            servers=settings.NATS_URL,
            error_cb=self._error_cb,
            disconnected_cb=self._disconnected_cb,
            reconnected_cb=self._reconnected_cb,
            closed_cb=self._closed_cb,
            max_reconnect_attempts=-1,   # retry indefinitely
            reconnect_time_wait=2,       # seconds between retries
            connect_timeout=10,
            token=settings.NATS_TOKEN
        )

        self._js = self._nc.jetstream()
        logger.info("NATS connected. Server: %s", self._nc.connected_url)

        await self._provision_streams()

    async def drain(self) -> None:
        if self._nc and not self._nc.is_closed:
            logger.info("Draining NATS connection...")
            await self._nc.drain()

    async def close(self) -> None:
        if self._nc and not self._nc.is_closed:
            logger.info("Closing NATS connection...")
            await self._nc.close()
    

    async def _provision_streams(self) -> None:
        if self._nc is None:
            return

        jsm = self._nc.jsm()
        config = StreamConfig(
            name=_STREAM_NAME,
            subjects=_STREAM_SUBJECTS,
            retention=RetentionPolicy.LIMITS,
            storage=StorageType.FILE,
            max_age=_MAX_AGE,
            max_msgs=_MAX_MSGS,
            max_bytes=_MAX_BYTES,
            num_replicas=_NUM_REPLICAS,
            duplicate_window=_DUPLICATE_WINDOW,
        )

        try:
            await jsm.stream_info(_STREAM_NAME)
            logger.info("Stream '%s' already exists — updating config.", _STREAM_NAME)
            await jsm.update_stream(config=config)
        except NotFoundError:
            logger.info("Stream '%s' not found — creating.", _STREAM_NAME)
            await jsm.add_stream(config=config)

        logger.info("Stream '%s' provisioned successfully.", _STREAM_NAME)

    async def health_check(self) -> dict:
        if self._nc is None or self._nc.is_closed:
            return {"status": "disconnected"}

        try:
            info = await self._nc.jsm().stream_info(name=_STREAM_NAME)
            return {
                "status": "connected",
                "server": str(self._nc.connected_url),
                "stream": {
                    "name": info.config.name,
                    "messages": info.state.messages,
                    "bytes": info.state.bytes,
                    "consumer_count": info.state.consumer_count,
                },
            }
        except Exception as exc:
            logger.warning("NATS health check failed: %s", exc)
            return {"status": "degraded", "error": str(exc)}

    async def _error_cb(self, exc: Exception) -> None:
        logger.error("NATS error: %s", exc)

    async def _disconnected_cb(self) -> None:
        logger.warning("NATS disconnected.")

    async def _reconnected_cb(self) -> None:
        logger.info("NATS reconnected to %s", self._nc.connected_url if self._nc else "unknown")

    async def _closed_cb(self) -> None:
        logger.info("NATS connection closed.")
