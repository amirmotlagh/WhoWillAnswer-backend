from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.category import CategoryInfo
from app.core.interfaces.category import ICategoryRepository
from app.infrastructure.database.models import Category


class CategoryRepository(ICategoryRepository):
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

	async def create_category(self, category_info: CategoryInfo) -> CategoryInfo:
		category_data = category_info.model_dump(exclude={'id'})
		new_category = Category(**category_data)
		self.session.add(new_category)
		await self.session.flush()
		created_category = await self.get_category_by_id(new_category.id)
		if not created_category:
			raise RuntimeError('Failed to retrieve the newly created category')
		return created_category
