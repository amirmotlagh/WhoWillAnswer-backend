from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.question import QuestionInfo
from app.core.interfaces.question import IQuestionRepository
from app.infrastructure.database.models import Question


class QuestionRepository(IQuestionRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_question_by_id(self, question_id: int) -> QuestionInfo | None:
		stmt = (
			select(Question)
			.options(selectinload(Question.category))
			.where(Question.id == question_id)
		)
		result = await self.session.execute(stmt)
		question = result.scalar_one_or_none()
		if question:
			return QuestionInfo.model_validate(question)
		return None

	async def create_question(self, question_info: QuestionInfo) -> QuestionInfo:
		question_data = question_info.model_dump(exclude={'id', 'category'})
		question = Question(**question_data)
		self.session.add(question)
		await self.session.flush()

		created_question = await self.get_question_by_id(question.id)
		if not created_question:
			raise RuntimeError('Failed to retrieve the newly created question')
		return created_question

	async def update_question(self, question: QuestionInfo) -> QuestionInfo | None:
		if not question.id:
			raise ValueError('Question ID is required for update')

		stmt = (
			update(Question)
			.where(Question.id == question.id)
			.values(question.model_dump(exclude={'id', 'category'}))
		)
		await self.session.execute(stmt)
		await self.session.commit()

		return await self.get_question_by_id(question.id)

	async def get_unapproved_questions(self) -> list[QuestionInfo]:
		stmt = (
			select(Question)
			.options(selectinload(Question.category))
			.where(Question.approved == False)  # noqa: E712
		)
		result = await self.session.execute(stmt)
		questions = result.scalars().all()
		if questions:
			return [QuestionInfo.model_validate(question) for question in questions]
		return []

	async def get_approved_questions_of_category(self, category_id: int) -> list[QuestionInfo]:
		stmt = (
			select(Question)
			.options(selectinload(Question.category))
			.where(Question.category_id == category_id, Question.approved == True)  # noqa: E712
		)
		result = await self.session.execute(stmt)
		questions = result.scalars().all()
		if questions:
			return [QuestionInfo.model_validate(question) for question in questions]
		return []
