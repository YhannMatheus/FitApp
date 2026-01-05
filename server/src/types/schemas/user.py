from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from uuid import UUID
from typing import Optional
from src.types.models.user import GenderEnum, ActivityLevelEnum, RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    birth_date: date
    height_cm: float
    gender: GenderEnum
    activity_level: ActivityLevelEnum


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    goal: Optional[float] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    height_cm: Optional[float] = None
    gender: Optional[GenderEnum] = None
    activity_level: Optional[ActivityLevelEnum] = None
    goal: Optional[float] = None


class UserRead(UserBase):
    id: UUID
    role: RoleEnum
    goal: Optional[float]
    activates_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
