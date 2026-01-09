from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from src.types.enums.exercise import ExerciseTypeEnum, IntensityLevelEnum, ExercisseNameEnum


class ExerciseCreate(BaseModel):
    workout_id: UUID
    name: ExercisseNameEnum
    type: ExerciseTypeEnum
    intensity: IntensityLevelEnum


class ExerciseUpdate(BaseModel):
    name: Optional[ExercisseNameEnum]
    type: Optional[ExerciseTypeEnum] = None
    intensity: Optional[IntensityLevelEnum] = None


class ExerciseRead(BaseModel):
    id: UUID
    workout_id: UUID
    name: ExercisseNameEnum
    type: ExerciseTypeEnum
    intensity: IntensityLevelEnum
    calories_burned: float
    created_at: datetime

    class Config:
        from_attributes = True
