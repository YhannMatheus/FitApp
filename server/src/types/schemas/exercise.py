from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from src.types.enums.workout import (
    ExerciseTypeEnum,
    ExerciseCategoryEnum,
    IntensityLevelEnum,
)


class SetBase(BaseModel):
    reps: Optional[int] = Field(None, ge=1)
    weight: Optional[float] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=1)


class SetCreate(SetBase):
    pass


class SetUpdate(SetBase):
    pass


class SetSchema(SetBase):
    id: UUID
    exercise_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    exercise_type: ExerciseTypeEnum
    category: ExerciseCategoryEnum
    intensity: IntensityLevelEnum


class ExerciseCreate(ExerciseBase):
    sets: List[SetCreate] = Field(default_factory=list)


class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    exercise_type: Optional[ExerciseTypeEnum] = None
    category: Optional[ExerciseCategoryEnum] = None
    intensity: Optional[IntensityLevelEnum] = None


class ExerciseSchema(ExerciseBase):
    id: UUID
    workout_id: UUID
    sets: List[SetSchema] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
