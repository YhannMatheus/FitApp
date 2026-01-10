from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from src.types.enums.exercise import ExerciseTypeEnum, IntensityLevelEnum, ExercisseNameEnum
from src.types.schemas.set import SetRead

class ExerciseCreate(BaseModel):
    workout_id: UUID
    name: ExercisseNameEnum
    type: ExerciseTypeEnum
    intensity: IntensityLevelEnum

class ExerciseUpdate(BaseModel):
    name: Optional[ExercisseNameEnum] = None
    type: Optional[ExerciseTypeEnum] = None
    intensity: Optional[IntensityLevelEnum] = None

class ExerciseMinimal(BaseModel):
    id: UUID
    name: str
    type: str
    intensity: str
    calories_burned: float
    
    class Config:
        from_attributes = True

class ExerciseRead(BaseModel):
    id: UUID
    workout_id: UUID
    name: ExercisseNameEnum
    type: ExerciseTypeEnum
    intensity: IntensityLevelEnum
    sets: Optional[List[SetRead]] = []
    calories_burned: float
    created_at: datetime

    class Config:
        from_attributes = True
