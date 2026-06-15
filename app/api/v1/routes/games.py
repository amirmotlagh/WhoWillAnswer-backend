
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.game import GameInfo
from app.core.services.game_service import initiate_new_game
from app.infrastructure.database.repositories.game_repository import GameRepository
from app.infrastructure.database.session import get_database_session
from app.logger import get_logger
from app.schemas.game import GameCreate
from app.infrastructure.database.repositories.user_repository import UserRepository


logger = get_logger(__name__)

game_router = APIRouter(prefix="/game", tags=["game"])

@game_router.post("/initiate/{creator_id}", summary="Initiate a new game")
async def initiate_new_game_endpoint(creator_id: int, game_data: GameCreate, request: Request, session: AsyncSession = Depends(get_database_session)): #TODO: this should get game data from request, just for test
    user_repo = UserRepository(session)
    game_repo = GameRepository(session)
    publisher = request.app.state.publisher
    await initiate_new_game(creator_id, game_data, user_repo, game_repo, publisher)
    return {"message": "Game initiated successfully"}
