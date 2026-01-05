from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from src.types.models.exercise import ExerciseTypeEnum, IntensityLevelEnum


class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: ExerciseTypeEnum
    intensity: IntensityLevelEnum


class ExerciseCreate(ExerciseBase):
    workout_id: UUID


class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[ExerciseTypeEnum] = None
    intensity: Optional[IntensityLevelEnum] = None


class ExerciseRead(ExerciseBase):
    id: UUID
    workout_id: UUID
    calories_burned: float
    created_at: datetime

    class Config:
        from_attributes = True
