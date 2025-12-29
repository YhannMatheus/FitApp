from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.types.schemas.user import UserRead
from src.services.user_services import UserService
from src.core.auth.security import get_current_user
from src.database.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(user=Depends(get_current_user)):
    return user
