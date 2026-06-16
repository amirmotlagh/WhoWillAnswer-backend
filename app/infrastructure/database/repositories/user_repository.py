
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import User
from app.core.domain.user import UserInfo

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> UserInfo | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return UserInfo.model_validate(user)
        return None


    async def create_user(self, user_data: UserInfo) -> UserInfo:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.flush()
        return UserInfo.model_validate(user)

    async def update_user(self, user_id: int, user_data: dict) -> UserInfo | None:
        raise NotImplementedError("UserRepository.update_user is not implemented yet")
