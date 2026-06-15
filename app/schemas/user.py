from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    phone_number: str | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: str | None = None
    phone_number: str | None = None

class UserInfoForGame(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str | None = None