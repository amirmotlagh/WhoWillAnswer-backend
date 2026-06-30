from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_user
from app.core.services.game_service import initiate_new_game
from app.infrastructure.database.repositories.category_repository import CategoryRepository
from app.infrastructure.database.repositories.game_repository import GameRepository
from app.infrastructure.database.session import get_database_session
from app.logger import get_logger
from app.schemas.game import GameCreate, GameResponse
from app.schemas.response import StandardResponse
from app.schemas.user import UserData


logger = get_logger(__name__)

game_router = APIRouter(prefix='/game', tags=['game'])


@game_router.post(
	'/initiate/',
	summary='Initiate a new game',
	status_code=201,
	response_model=StandardResponse[GameResponse],
)
async def initiate_new_game_endpoint(
	user: Annotated[UserData, Depends(require_user)],
	game_data: GameCreate,
	session: Annotated[AsyncSession, Depends(get_database_session)],
	request: Request,
):
	try:
		game_repo = GameRepository(session)
		category_repo = CategoryRepository(session)
		publisher = getattr(request.app.state, 'publisher', None)
		if publisher is None:
			logger.error('Publisher not available')
			raise HTTPException(status_code=503, detail='Game service temporarily unavailable')
		created_game = await initiate_new_game(user, game_data, game_repo, category_repo, publisher)
		return StandardResponse(message='Game initiated successfully', payload=created_game)
	except ValueError as e:
		logger.error(f'Invalid game data: {e}')
		raise HTTPException(status_code=404, detail='Invalid game data')
	except HTTPException as e:
		logger.error(f'HTTP error occurred: {e}')
		raise
	except SQLAlchemyError as e:
		logger.error(f'Database error occurred: {e}')
		raise HTTPException(status_code=500, detail='Database error occurred')
	except Exception as e:
		logger.error(f'Unexpected error occurred: {e}')
		raise HTTPException(status_code=500, detail='Internal server error')
