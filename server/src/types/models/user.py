from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Date, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base

if TYPE_CHECKING:
    from .body_assessment import BodyAssessment
    from .workout import Workout


class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ActivityLevelEnum(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    HIGH = "high"
    ATHLETE = "athlete"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    birth_date: Mapped[date]
    height_cm: Mapped[float]
    sex: Mapped[SexEnum] = mapped_column(SQLEnum(SexEnum, name="sex_enum"))
    activity_level: Mapped[ActivityLevelEnum] = mapped_column(
        SQLEnum(ActivityLevelEnum, name="activity_level_enum")
    )
    goal: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    body_assessments: Mapped[list["BodyAssessment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    workouts: Mapped[list["Workout"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
