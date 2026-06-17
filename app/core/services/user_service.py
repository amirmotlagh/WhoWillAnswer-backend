from app.core.domain.user import UserInfo
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse


async def create_user(user_data: UserCreate, user_repo: UserRepository) -> UserResponse:
	user_info = UserInfo(**user_data.model_dump())
	user = await user_repo.create_user(user_info)
	return UserResponse.model_validate(user)
