
from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserInfoForGame


class GameCreate(BaseModel):
    name: str
    min_players: int
    max_players: int
    category_id: int
    private: bool = False
    password: str | None = None
    max_timeout: int = 120

class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creator: UserInfoForGame
    players: list[UserInfoForGame]
    min_players: int
    max_players: int
    category_id: int
    private: bool
    max_timeout: int