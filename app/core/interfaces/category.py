from abc import ABC, abstractmethod

from app.core.domain.category import CategoryInfo


class ICategoryRepository(ABC):
	@abstractmethod
	async def get_category_by_id(self, category_id: int) -> CategoryInfo | None: ...

	@abstractmethod
	async def get_all_categories(self) -> list[CategoryInfo]: ...

	@abstractmethod
	async def create_category(self, category_info: CategoryInfo) -> CategoryInfo: ...
