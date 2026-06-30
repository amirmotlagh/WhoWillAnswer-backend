from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services import user_service
from app.core.exceptions import (
	InactiveUserError,
	InvalidCredentialsError,
	UserAlreadyExistsError,
	UserLacksRolesError,
)
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.session import get_database_session
from app.logger import get_logger
from app.schemas.response import StandardResponse
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse


logger = get_logger(__name__)

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.post(
	'/create/',
	summary='Create a new user',
	status_code=201,
	response_model=StandardResponse[UserResponse],
)
async def create_user(
	user_data: UserCreate, session: Annotated[AsyncSession, Depends(get_database_session)]
):
	try:
		user_repo = UserRepository(session)
		user = await user_service.create_user(user_data, user_repo)
		return StandardResponse(message='User created successfully', payload=user)
	except UserAlreadyExistsError as e:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
	except Exception:
		logger.error('Error creating user')
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not create user.'
		)


@user_router.post('/login/', summary='Login a user', status_code=200, response_model=Token)
async def login_user(
	user_data: UserLogin, session: Annotated[AsyncSession, Depends(get_database_session)]
):
	try:
		user_repo = UserRepository(session)
		token = await user_service.login_user_with_password(user_data, user_repo)
		return token
	except InvalidCredentialsError as e:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=str(e),
			headers={'WWW-Authenticate': 'Bearer'},
		)
	except InactiveUserError as e:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
	except UserLacksRolesError as e:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
	except Exception:
		logger.error('Error during login')
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail='An unexpected error occurred during login.',
		)
