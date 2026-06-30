from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.session import get_database_session
from app.schemas.user import UserData
from app.utils.enums import UserRoles
from app.utils.jwt import decode_token

security = HTTPBearer()


async def get_current_user(
	credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
	session: Annotated[AsyncSession, Depends(get_database_session)],
) -> UserData:
	token = credentials.credentials
	token_data = await decode_token(token)

	user_repo = UserRepository(session)
	user = await user_repo.get_user_by_id(token_data.user_id)

	if user is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

	if not user.is_active:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive user')

	return UserData.model_validate(user)


class RoleChecker:
	def __init__(self, allowed_roles: list[UserRoles]):
		self.allowed_roles = allowed_roles

	async def __call__(self, user: UserData = Depends(get_current_user)) -> UserData:
		has_permission = any(role in self.allowed_roles for role in user.roles)

		if not has_permission:
			raise HTTPException(
				status_code=403, detail=f'User does not have required roles: {self.allowed_roles}'
			)

		return user


require_admin = RoleChecker([UserRoles.ADMIN])
require_moderator = RoleChecker([UserRoles.ADMIN, UserRoles.MODERATOR])
require_user = RoleChecker([UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.USER])
