
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services import user_service
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.session import get_database_session
from app.logger import get_logger
from app.schemas.response import UserCreateResponse
from app.schemas.user import UserCreate


logger = get_logger(__name__)

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/create/", summary="Create a new user", status_code=201, response_model=UserCreateResponse)
async def create_user(user_data: UserCreate, session: Annotated[AsyncSession, Depends(get_database_session)]):
    user_repo = UserRepository(session)
    user = await user_service.create_user(user_data, user_repo)
    
    return {"message": "User created successfully", "payload": user}