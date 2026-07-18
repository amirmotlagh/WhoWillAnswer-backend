from abc import ABC, abstractmethod

from app.core.domain.question import QuestionInfo


class IQuestionRepository(ABC):
	@abstractmethod
	async def get_question_by_id(self, question_id: int) -> QuestionInfo | None: ...

	@abstractmethod
	async def create_question(self, question_info: QuestionInfo) -> QuestionInfo: ...

	@abstractmethod
	async def update_question(self, question: QuestionInfo) -> QuestionInfo | None: ...

	@abstractmethod
	async def get_unapproved_questions(self) -> list[QuestionInfo]: ...

	@abstractmethod
	async def get_approved_questions_of_category(self, category_id: int) -> list[QuestionInfo]: ...
