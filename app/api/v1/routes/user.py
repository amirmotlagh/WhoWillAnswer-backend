

from fastapi import APIRouter, Depends

from app.core.services import user_service
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.session import get_database_session
from app.logger import get_logger
from app.schemas.user import UserCreate, UserResponse


logger = get_logger(__name__)

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/create/", summary="Create a new user", status_code=201)
async def create_user(user_data: UserCreate, session=Depends(get_database_session)):
    user_repo = UserRepository(session)
    user = await user_service.create_user(user_data, user_repo)
    
    return {"message": "User created successfully", "user": user}