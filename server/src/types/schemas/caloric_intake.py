from pydantic import BaseModel, Field
from datetime import date as Date, datetime
from uuid import UUID
from typing import Optional


class CaloricIntakeBase(BaseModel):
    date: Date
    calories_consumed: float = Field(default=0.0, ge=0)
    protein_grams: float = Field(default=0.0, ge=0)
    carbs_grams: float = Field(default=0.0, ge=0)
    fats_grams: float = Field(default=0.0, ge=0)


class CaloricIntakeCreate(CaloricIntakeBase):
    user_id: UUID


class CaloricIntakeUpdate(BaseModel):
    date: Optional[Date] = None
    calories_consumed: Optional[float] = Field(None, ge=0)
    protein_grams: Optional[float] = Field(None, ge=0)
    carbs_grams: Optional[float] = Field(None, ge=0)
    fats_grams: Optional[float] = Field(None, ge=0)


class CaloricIntakeRead(CaloricIntakeBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
