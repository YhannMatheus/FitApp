from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from src.types.enums.workout import TrainingTypeEnum


class WorkoutCreate(BaseModel):
    user_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    type: TrainingTypeEnum
    start_time: datetime


class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[TrainingTypeEnum] = None
    end_time: Optional[datetime] = None


class WorkoutRead(BaseModel):
    id: UUID
    user_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    type: TrainingTypeEnum
    start_time: datetime
    total_calories_burned: float
    end_time: Optional[datetime]
    create_at: datetime

    class Config:
        from_attributes = True


class WorkoutComplete(BaseModel):
    end_time: datetime
