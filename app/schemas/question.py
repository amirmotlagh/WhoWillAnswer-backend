from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.category import CategoryResponse


class QuestionCreate(BaseModel):
	text: str
	category_id: int
	answers: list[str] = Field(..., min_length=4, max_length=4)
	correct_answer: int

	@model_validator(mode='after')
	def validate_correct_answer_index(self) -> Self:
		if not (0 <= self.correct_answer < len(self.answers)):
			raise ValueError('correct_answer must be a valid index for the answers list')
		return self


class QuestionResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	text: str
	category: CategoryResponse
	answers: list[str]
	correct_answer: int
	approved: bool
