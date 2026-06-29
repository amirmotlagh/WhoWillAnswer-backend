from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.enums import UserRoles


class UserCreate(BaseModel):
	username: str = Field(..., min_length=1, max_length=100)
	email: EmailStr = Field(..., max_length=255)
	full_name: str | None = None
	phone_number: str | None = None
	password: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
	username: str = Field(..., min_length=1, max_length=100)
	password: str = Field(..., min_length=1, max_length=100)


class UserResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	username: str
	email: EmailStr
	full_name: str | None = None
	phone_number: str | None = None


class UserInfoForGame(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	username: str
	full_name: str | None = None


class UserTokenResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	username: str
	email: EmailStr
	full_name: str | None = None
	phone_number: str | None = None
	token_type: str


class Token(BaseModel):
	access_token: str
	refresh_token: str


class TokenData(BaseModel):
	user_id: int
	username: str
	email: EmailStr
	full_name: str | None = None
	phone_number: str | None = None
	is_active: bool | None = None
	roles: list[UserRoles] = []


class UserData(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	username: str
	email: EmailStr
	full_name: str | None = None
	phone_number: str | None = None
	is_active: bool | None = None
	roles: list[UserRoles] = []
