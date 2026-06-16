from pydantic import BaseModel

from app.schemas.game import GameResponse
from app.schemas.user import UserResponse


class GameInitiateResponse(BaseModel):
    message: str
    payload: GameResponse


class UserCreateResponse(BaseModel):
    message: str
    payload: UserResponse