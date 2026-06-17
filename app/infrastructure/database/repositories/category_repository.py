from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.category import CategoryInfo
from app.infrastructure.database.models import Category


class CategoryRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_category_by_id(self, category_id: int) -> CategoryInfo | None:
		result = await self.session.execute(select(Category).where(Category.id == category_id))
		category = result.scalar_one_or_none()
		if category:
			return CategoryInfo.model_validate(category)
		return None

	async def get_all_categories(self) -> list[CategoryInfo]:
		result = await self.session.execute(select(Category))
		return [CategoryInfo.model_validate(category) for category in result.scalars().all()]
