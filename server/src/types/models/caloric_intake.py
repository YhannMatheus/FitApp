from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.types.models.base import Base

if TYPE_CHECKING:
    from .user import User


class CaloricIntake(Base):
    __tablename__ = "caloric_intakes"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    calories: Mapped[float]
    protein_g: Mapped[float | None]
    carbs_g: Mapped[float | None]
    fat_g: Mapped[float | None]

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="caloric_intakes")
