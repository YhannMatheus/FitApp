from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base

if TYPE_CHECKING:
    from .user import User
    from .exercise import Exercise


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    total_calories_burned: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="workouts")

    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    exercises: Mapped[list["Exercise"]] = relationship(
        back_populates="workout", cascade="all, delete-orphan"
    )
