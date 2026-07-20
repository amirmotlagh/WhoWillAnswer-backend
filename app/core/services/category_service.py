import uuid

from fastapi.encoders import jsonable_encoder

from app.core.interfaces.category import ICategoryRepository

from app.infrastructure.cache.category_cache import get_category_cache, set_category_cache
from app.infrastructure.messaging.publisher import EventPublisher
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.domain.category import CategoryInfo
from app.utils.exceptions import CreationFailedException
from app.infrastructure.messaging.subjects import Subjects


class CategoryService:
	def __init__(self, category_repo: ICategoryRepository, publisher: EventPublisher):
		self.category_repo = category_repo
		self.publisher = publisher

	async def get_all_categories(self) -> list[CategoryResponse]:
		categories = await get_category_cache()
		if not categories:
			categories = await self.category_repo.get_all_categories()
			if categories:
				await set_category_cache(categories)

		return [CategoryResponse.model_validate(cat) for cat in categories] if categories else []

	async def create_new_category(self, category_data: CategoryCreate) -> CategoryResponse:
		category_info = CategoryInfo(**category_data.model_dump())
		category = await self.category_repo.create_category(category_info)
		if not category:
			raise CreationFailedException('Failed to create a new category')

		category_dict = jsonable_encoder(category)
		publisher_payload = {'category_data': category_dict}
		event_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f'category_created_{category.id}'))
		await self.publisher.publish(
			subject=Subjects.CATEGORY_CREATED, payload=publisher_payload, event_id=event_id
		)
		return CategoryResponse(**category_dict)
