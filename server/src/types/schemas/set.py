from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


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
