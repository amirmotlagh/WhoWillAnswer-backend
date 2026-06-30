from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import UserRoles


class UserInfo(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int | None = None
	email: str
	username: str
	roles: list[UserRoles] = Field(default_factory=list)
	full_name: str | None = None
	is_active: bool = True
	phone_number: str | None = None
	password: str | None = None
