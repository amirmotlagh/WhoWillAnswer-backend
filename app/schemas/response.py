from typing import Generic, TypeVar
from pydantic import BaseModel, Field

PayloadType = TypeVar('PayloadType')


class StandardResponse(BaseModel, Generic[PayloadType]):
	message: str = Field(
		..., description='A human-readable message indicating the result of the operation.'
	)
	payload: PayloadType | None = Field(None, description='The data returned by the endpoint.')
