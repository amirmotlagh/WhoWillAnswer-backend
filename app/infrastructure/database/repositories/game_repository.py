from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import selectinload

from app.core.domain.game import GameInfo
from app.infrastructure.database.models import Game, GameState, game_players


class GameRepository:
    def __init__(self, session):
        self.session = session

    async def create_game(self, game_info: GameInfo) -> GameInfo:
        game_data = game_info.model_dump(exclude={"id", "players"})
        game = Game(**game_data)
        self.session.add(game)
        await self.session.flush()
        
        created_game = await self.get_game(game.id)
        if not created_game:
            raise RuntimeError("Failed to retrieve the newly created game")
        return created_game
    
    async def get_active_games(self) -> list[GameInfo]:
        stmt = select(Game).options(selectinload(Game.players)).where(Game.state == GameState.ACTIVE)
        result = await self.session.execute(stmt)
        games = result.scalars().all()
        if games:
            return [GameInfo.model_validate(game) for game in games]
        return []


    async def add_players_to_game(self, game_id: int, player_ids: list[int]) -> GameInfo | None:
        if not player_ids:
            return await self.get_game(game_id)

        values = [{"game_id": game_id, "user_id": pid} for pid in player_ids]
        
        stmt = pg_insert(game_players).values(values).on_conflict_do_nothing()
        
        await self.session.execute(stmt)
        
        return await self.get_game(game_id)

    async def get_game(self, game_id: int) -> GameInfo | None:
        stmt = select(Game).options(selectinload(Game.players)).where(Game.id == game_id)
        result = await self.session.execute(stmt)
        game = result.scalar_one_or_none()
        if game:
            return GameInfo.model_validate(game)
        return None


    async def update_game(self, game_id: int, game_info: GameInfo):
        # Implement logic to update an existing game in the database
        raise NotImplementedError("GameRepository.update_game is not implemented yet")

    async def delete_game(self, game_id: int):
        # Implement logic to delete a game from the database
        raise NotImplementedError("GameRepository.delete_game is not implemented yet")