from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_question_service, require_user, require_moderator
from app.core.services.question_service import QuestionService
from app.logger import get_logger
from app.schemas.question import QuestionCreate, QuestionResponse
from app.schemas.response import StandardResponse
from app.schemas.user import UserData
from app.utils.exceptions import CreationFailedException, EntityNotFoundException


logger = get_logger(__name__)

question_router = APIRouter(prefix='/question', tags=['question'])


@question_router.post(
	'/add/',
	summary='add new question to questions pool',
	status_code=201,
	response_model=StandardResponse[QuestionResponse],
)
async def add_new_question(
	_: Annotated[UserData, Depends(require_user)],
	question_data: QuestionCreate,
	question_service: Annotated[QuestionService, Depends(get_question_service)],
):

	try:
		created_question = await question_service.create_new_question(question_data)
		return StandardResponse(message='Question added successfully', payload=created_question)
	except EntityNotFoundException as e:
		logger.error(f'Entity not found: {e}')
		raise HTTPException(status_code=404, detail=str(e))
	except CreationFailedException as e:
		logger.error(f'Failed to create question: {e}')
		raise HTTPException(status_code=500, detail=str(e))
	except ValueError as e:
		logger.error(f'Invalid question data: {e}')
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		logger.error(f'Unexpected error occurred: {e}')
		raise HTTPException(status_code=500, detail='Internal server error')


@question_router.get(
	'/unapproved/',
	summary='get unapproved questions',
	status_code=200,
	response_model=StandardResponse[list[QuestionResponse]],
)
async def get_unapproved_questions(
	_: Annotated[UserData, Depends(require_moderator)],
	question_service: Annotated[QuestionService, Depends(get_question_service)],
):

	questions = await question_service.unapproved_questions()
	if not questions:
		raise HTTPException(status_code=404, detail='No unapproved questions found')
	return StandardResponse(
		message='Unapproved questions retrieved successfully', payload=questions
	)


@question_router.patch(
	'/{question_id}/approve/',
	summary='approve a question',
	status_code=200,
	response_model=StandardResponse[None],
)
async def approve_a_question(
	_: Annotated[UserData, Depends(require_moderator)],
	question_id: int,
	question_service: Annotated[QuestionService, Depends(get_question_service)],
):
	try:
		await question_service.approve_question(question_id)
		return StandardResponse(message='Question approved successfully', payload=None)
	except EntityNotFoundException as e:
		logger.error(f'Question not found: {e}')
		raise HTTPException(status_code=404, detail='Question not found')
