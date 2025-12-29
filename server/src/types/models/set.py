from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base

if TYPE_CHECKING:
    from .exercise import Exercise


class Set(Base):
    __tablename__ = "sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    reps: Mapped[int | None]
    weight: Mapped[float | None]
    duration: Mapped[int | None]
    calories_burned: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE")
    )

    exercise: Mapped["Exercise"] = relationship(back_populates="sets")
