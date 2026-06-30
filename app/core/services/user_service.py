from datetime import timedelta

from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.core.domain.user import UserInfo
from app.core.exceptions import (
	InactiveUserError,
	InvalidCredentialsError,
	UserAlreadyExistsError,
	UserLacksRolesError,
)
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse
from app.utils.enums import UserRoles
from app.utils.jwt import TokenInputData, create_access_token, create_refresh_token
from app.utils.password import Hash


async def create_user(user_data: UserCreate, user_repo: UserRepository) -> UserResponse:
	try:
		user_info = UserInfo(**user_data.model_dump())
		user_info.password = Hash.get_hashed_password(user_data.password)
		user_info.roles = [UserRoles.USER.value]
		user = await user_repo.create_user(user_info)
		return UserResponse.model_validate(user)
	except IntegrityError:
		await user_repo.session.rollback()
		raise UserAlreadyExistsError(
			'A user with this username, phone number, or email already exists.'
		)


async def login_user_with_password(user_data: UserLogin, user_repo: UserRepository) -> Token:
	user = await user_repo.get_user_by_username(user_data)
	if not user or not user.password or not Hash.verify(user.password, user_data.password):
		raise InvalidCredentialsError('Invalid username or password')

	if not user.id or not user.username or not user.email:
		raise ValueError('Incomplete user data in database')
	if not user.is_active:
		raise InactiveUserError('User account is inactive')
	if not user.roles or len(user.roles) == 0:
		raise UserLacksRolesError('User has no roles assigned')

	token_data = TokenInputData(user_id=user.id)

	access_token = create_access_token(
		token_data, timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
	)
	refresh_token = create_refresh_token(
		token_data, timedelta(minutes=settings.AUTH_REFRESH_TOKEN_EXPIRE_MINUTES)
	)
	return Token(access_token=access_token, refresh_token=refresh_token)
