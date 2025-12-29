from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.types.schemas.auth import LoginSchema, TokenSchema
from src.types.schemas.user import UserRead, UserCreateSchema
from src.services.user_services import UserService
from src.services.auth_services import AuthService
from src.database.session import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    user = await UserService.create(db, data)
    return user


@router.post("/login", response_model=TokenSchema)
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(db, data.email, data.password)
