

from pydantic import BaseModel, ConfigDict


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    email: str
    username: str
    full_name: str | None = None
    is_active: bool = True
    phone_number: str | None = None
