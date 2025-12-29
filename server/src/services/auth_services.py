from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.services.user_services import UserService
from src.core.auth.security import Password
from src.core.auth.token import AccessToken
from src.types.schemas.auth import TokenSchema


class AuthService:
    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> TokenSchema:
        user = await UserService.get_by_email(db, email)

        if not user or not Password.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = AccessToken(str(user.id)).generate()

        return TokenSchema(access_token=token)
