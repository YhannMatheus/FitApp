from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.types.models.user import User
from src.types.schemas.user import UserCreateSchema
from server.src.core.auth.security import Password

class UserService:
    @staticmethod
    async def create(db: AsyncSession, data: UserCreateSchema) -> User:
        user = User(
            name=data.name,
            email=data.email,
            password_hash=Password.hash(data.password),
            sex=data.sex,
            birth_date=data.birth_date,
            height=data.height_cm,
            weight=data.weight_kg,
            activity_level=data.activity_level,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
