from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base

if TYPE_CHECKING:
    from .user import User


class BodyAssessment(Base):
    __tablename__ = "body_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    date: Mapped[Date] = mapped_column(Date)

    weight_kg: Mapped[float]

    waist_cm: Mapped[float | None]
    hip_cm: Mapped[float | None]
    chest_cm: Mapped[float | None]
    arm_cm: Mapped[float | None]
    thigh_cm: Mapped[float | None]
    calf_cm: Mapped[float | None]

    body_fat_percent: Mapped[float | None]
    lean_mass_kg: Mapped[float | None]

    bmi: Mapped[float | None]
    bmr: Mapped[float | None]
    tdee: Mapped[float | None]

    user: Mapped["User"] = relationship(back_populates="body_assessments")
