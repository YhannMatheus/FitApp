from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class SetCreate(BaseModel):
    exercise_id: UUID
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0, description="Peso em kg")
    duration: Optional[int] = Field(None, ge=0, description="Duração em segundos")


class SetUpdate(BaseModel):
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=0)


class SetRead(BaseModel):
    id: UUID
    exercise_id: UUID
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0, description="Peso em kg")
    duration: Optional[int] = Field(None, ge=0, description="Duração em segundos")
    calories_burned: float
    created_at: datetime

    class Config:
        from_attributes = True
