from typing import Any

from app.infrastructure.cache.redis_client import redis_client
from app.schemas.response import StandardResponse
from fastapi import APIRouter, HTTPException, Request, status

from app.logger import get_logger

logger = get_logger(__name__)
health_router = APIRouter(prefix='/health', tags=['health'])


@health_router.get(
	'/', summary='Check application health', response_model=StandardResponse[dict[str, str]]
)
async def check_app_health():
	return StandardResponse(message='Application is healthy', payload={'status': 'ok'})


@health_router.get(
	'/redis', summary='Check Redis health', response_model=StandardResponse[dict[str, str]]
)
async def is_redis_available():
	try:
		ok_state = await redis_client.health_check()
		if not ok_state:
			raise HTTPException(
				status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
				detail={
					'status': 'error',
					'service': 'redis',
					'message': 'Redis health check failed',
				},
			)
		return StandardResponse(message='Redis connection is healthy', payload={'status': 'ok'})
	except HTTPException:
		raise
	except Exception as e:
		logger.error(f'Error checking Redis health: {e}')
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail={'status': 'error', 'service': 'redis', 'message': 'Could not connect to Redis'},
		)


@health_router.get(
	'/nats/', summary='Check Nats health', response_model=StandardResponse[dict[str, Any]]
)
async def is_nats_available(request: Request):
	try:
		state = await request.app.state.nats.health_check()
		if state.get('status') != 'connected':
			raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=state)
		return StandardResponse(message='NATS connection is healthy', payload=state)
	except Exception as e:
		logger.error(f'Error checking NATS health: {e}')
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail={'status': 'error', 'service': 'nats'},
		)
