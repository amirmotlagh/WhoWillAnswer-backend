from fastapi import HTTPException

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.user import UserData
from app.utils.enums import UserRoles
from app.utils.jwt import decode_token

security = HTTPBearer()


async def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserData:
	token = credentials.credentials
	token_data = await decode_token(token)

	return UserData(
		id=token_data.user_id,
		username=token_data.username,
		email=token_data.email,
		phone_number=token_data.phone_number,
		full_name=token_data.full_name,
		roles=token_data.roles,
		is_active=token_data.is_active,
	)


class RoleChecker:
	def __init__(self, allowed_roles: list[str]):
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
