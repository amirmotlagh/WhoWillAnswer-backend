from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryInfo(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	description: Optional[str] = None
