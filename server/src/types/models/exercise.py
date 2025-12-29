from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base
from src.types.enums.workout import (
    ExerciseTypeEnum,
    ExerciseCategoryEnum,
    IntensityLevelEnum,
)

if TYPE_CHECKING:
    from .workout import Workout
    from .set import Set


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    description: Mapped[str | None] = mapped_column(String(500))
    exercise_type: Mapped[ExerciseTypeEnum]
    category: Mapped[ExerciseCategoryEnum]
    intensity: Mapped[IntensityLevelEnum]
    calories_burned: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=datetime.utcnow
    )

    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE")
    )

    workout: Mapped["Workout"] = relationship(back_populates="exercises")
    sets: Mapped[list["Set"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
