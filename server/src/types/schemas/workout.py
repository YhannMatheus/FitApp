from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from src.types.schemas.exercise import ExerciseCreate, ExerciseSchema


class WorkoutBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class WorkoutCreate(WorkoutBase):
    exercises: List[ExerciseCreate] = Field(default_factory=list)


class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class WorkoutSchema(WorkoutBase):
    id: UUID
    user_id: UUID
    calories_burned: float
    exercises: List[ExerciseSchema] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkoutSummarySchema(BaseModel):
    """Schema resumido para listagem"""

    id: UUID
    name: str
    calories_burned: float
    exercise_count: int
    created_at: datetime

    class Config:
        from_attributes = True
