from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.category import CategoryResponse
from app.schemas.user import UserInfoForGame


class GameCreate(BaseModel):
	name: str = Field(..., min_length=1, max_length=100)
	min_players: int = Field(..., ge=2, description='At least 2 players are required')
	max_players: int = Field(..., ge=2, le=10, description='Maximum number of players limit')
	category_id: int = Field(..., ge=1)
	private: bool = False
	password: str | None = None
	max_timeout: int = Field(
		default=120, gt=60, lt=600, description='Timeout in seconds must be between 60 and 600'
	)

	@model_validator(mode='after')
	def validate_max_players(self) -> Self:
		if self.min_players > self.max_players:
			raise ValueError('max_players must be greater than or equal to min_players')
		return self


class GameResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	creator: UserInfoForGame
	players: list[UserInfoForGame]
	min_players: int
	max_players: int
	category: CategoryResponse
	private: bool
	max_timeout: int
