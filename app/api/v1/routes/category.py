from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.category import CategoryCreate
from app.api.v1.dependencies import get_category_service, require_user, require_moderator
from app.core.services.category_service import CategoryService
from app.logger import get_logger
from app.schemas.category import CategoryResponse
from app.schemas.response import StandardResponse
from app.schemas.user import UserData
from app.utils.exceptions import CreationFailedException

logger = get_logger(__name__)

category_router = APIRouter(prefix='/category', tags=['category'])


@category_router.get(
	'/',
	summary='Get all categories',
	status_code=200,
	response_model=StandardResponse[list[CategoryResponse]],
)
async def get_all_categories(
	_: Annotated[UserData, Depends(require_user)],
	category_service: Annotated[CategoryService, Depends(get_category_service)],
):
	try:
		categories = await category_service.get_all_categories()
		return StandardResponse(message='Categories retrieved successfully', payload=categories)
	except Exception as e:
		logger.error(f'Unexpected error occurred: {e}')
		raise HTTPException(status_code=500, detail='Internal server error')


@category_router.post(
	'/',
	summary='Create a new category',
	status_code=201,
	response_model=StandardResponse[CategoryResponse],
)
async def create_new_category(
	_: Annotated[UserData, Depends(require_moderator)],
	category_data: CategoryCreate,
	category_service: Annotated[CategoryService, Depends(get_category_service)],
):
	try:
		created_category = await category_service.create_new_category(category_data)
		return StandardResponse(message='Category created successfully', payload=created_category)
	except CreationFailedException as e:
		logger.error(f'Failed to create category: {e}')
		raise HTTPException(status_code=500, detail='Failed to create category')
