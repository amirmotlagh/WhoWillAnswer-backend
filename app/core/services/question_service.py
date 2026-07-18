from app.core.interfaces.question import IQuestionRepository
from app.core.interfaces.category import ICategoryRepository
from app.schemas.question import QuestionCreate, QuestionResponse
from app.core.domain.question import QuestionInfo
from app.utils.exceptions import CreationFailedException, EntityNotFoundException


class QuestionService:
	def __init__(self, question_repo: IQuestionRepository, category_repo: ICategoryRepository):
		self.question_repo = question_repo
		self.category_repo = category_repo

	async def create_new_question(
		self,
		question_data: QuestionCreate,
	) -> QuestionResponse:
		category = await self.category_repo.get_category_by_id(question_data.category_id)
		if not category:
			raise EntityNotFoundException('category', question_data.category_id)
		question_info = QuestionInfo(**question_data.model_dump())
		question = await self.question_repo.create_question(question_info)
		if not question:
			raise CreationFailedException('Failed to create a new question')

		response = QuestionResponse(
			**question.model_dump(),
		)
		return response

	async def approve_question(self, question_id: int) -> None:
		question = await self.question_repo.get_question_by_id(question_id)
		if not question:
			raise EntityNotFoundException('question', question_id)
		question.approved = True
		await self.question_repo.update_question(question)

	async def unapproved_questions(self) -> list[QuestionResponse]:
		questions = await self.question_repo.get_unapproved_questions()
		if not questions:
			return []

		print(f'Unapproved questions retrieved: {questions}')

		return [QuestionResponse(**q.model_dump()) for q in questions]

	async def get_approved_questions_of_category(self, category_id: int) -> list[QuestionResponse]:
		questions = await self.question_repo.get_approved_questions_of_category(category_id)
		return [QuestionResponse(**q.model_dump()) for q in questions]
