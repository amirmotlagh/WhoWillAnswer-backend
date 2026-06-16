import uuid
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.core.domain.game import GameInfo
from app.infrastructure.database.repositories.game_repository import GameRepository
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.messaging.subjects import Subjects
from app.infrastructure.messaging.publisher import EventPublisher
from app.schemas.game import GameCreate, GameResponse
from app.schemas.user import UserInfoForGame


async def initiate_new_game(creator_id: int, game_data: GameCreate, user_repo: UserRepository, game_repo: GameRepository, publisher: EventPublisher) -> None:
    user = await user_repo.get_user_by_id(creator_id)
    if not user or not user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator user not found")
    
    #TODO: add more validation logic (e.g. check if category exists)

    game_info = GameInfo(**game_data.model_dump(), creator_id=creator_id)

    try:
        game = await game_repo.create_game(game_info)

        if not game or not game.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create game")

        game = await game_repo.add_players_to_game(game.id, [user.id])
        if not game:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add creator to the game")
        
        await game_repo.session.commit()
    except Exception:
        await game_repo.session.rollback()
        raise
    
    game_response = GameResponse(
        **game.model_dump(),
        creator=UserInfoForGame.model_validate(user)
    )

    game_dict = jsonable_encoder(game_response)
    event_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f"match_created_{game.id}"))
    await publisher.publish(subject=Subjects.MATCH_CREATED, payload={"game_data": game_dict}, event_id=event_id)
