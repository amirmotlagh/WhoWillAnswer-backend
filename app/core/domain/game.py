

from typing import Self
from pydantic import BaseModel, Field, model_validator, ConfigDict

from app.core.domain.user import UserInfo


class GameInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    creator_id: int = Field(..., gt=0, description="Must be a valid positive ID")
    name: str = Field(..., min_length=1, max_length=100)
    min_players: int = Field(..., ge=2, description="At least 2 players are required")
    max_players: int = Field(..., ge=2, le=10, description="Maximum number of players limit")
    max_timeout: int | None = Field(default=120, gt=60, lt=600, description="Timeout in seconds must be positive")
    category_id: int = Field(..., gt=0)
    password: str | None = None
    private: bool = False
    players: list[UserInfo] = []

    @model_validator(mode='after')
    def check_players_count(self) -> Self:
        if self.min_players > self.max_players:
            raise ValueError("max_players must be greater than or equal to min_players")
        return self

