from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryResponse


class QuestionInfo(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int | None = None
	text: str
	answers: list[str]
	correct_answer: int
	approved: bool = False
	category_id: int
	category: CategoryResponse | None = None
