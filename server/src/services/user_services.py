from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.types.models_old.user import User
from src.types.schemas.user import UserCreateSchema
from src.core.auth.security import Password


class UserService:
    @staticmethod
    async def create(db: AsyncSession, data: UserCreateSchema) -> User:
        from src.types.models_old.body_assessment import BodyAssessment
        from datetime import date

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=Password.hash(data.password),
            sex=data.sex,
            birth_date=data.birth_date,
            height_cm=data.height_cm,
            activity_level=data.activity_level,
            goal="maintain",  # Default goal
        )

        db.add(user)
        await db.flush()  # Flush to get user.id

        # Create initial body assessment
        body_assessment = BodyAssessment(
            user_id=user.id,
            date=date.today(),
            weight_kg=data.weight_kg,
        )
        db.add(body_assessment)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_latest_weight(db: AsyncSession, user_id: int) -> float:
        """Retorna o peso mais recente do usuário."""
        from src.types.models_old.body_assessment import BodyAssessment

        result = await db.execute(
            select(BodyAssessment.weight_kg)
            .where(BodyAssessment.user_id == user_id)
            .order_by(BodyAssessment.date.desc())
            .limit(1)
        )
        weight = result.scalar_one_or_none()
        return weight if weight else 70.0  # Default weight se não houver registro
