from pydantic import BaseModel, EmailStr, Field
from datetime import date as Date, datetime
from typing import Optional, List
from src.types.enums.user import GenderEnum, ActivityLevelEnum, RoleEnum
from src.types.schemas.workout import WorkoutRead
from src.types.schemas.body_assessment import BodyAssessmentBase

class UserProfile(BaseModel):
    token: str
    email: EmailStr
    name: str
    birth_date: Date
    height_cm: float
    gender: GenderEnum
    activity_level: ActivityLevelEnum
    role: RoleEnum
    created_at: datetime
    workouts : List[WorkoutRead]
    body_history: List[BodyAssessmentBase]