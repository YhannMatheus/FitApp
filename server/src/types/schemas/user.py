from datetime import date
from pydantic import BaseModel, EmailStr, Field
from src.types.enums.user import SexEnum, ActivityLevelEnum


class UserCreateSchema(BaseModel):
    name : str = Field(min_length=3, max_length=120)
    email : EmailStr
    password : str = Field(min_length=8)
    sex : SexEnum
    birth_date : date
    height_cm : float = Field(gt=0)
    weight_kg : float = Field(gt=0)
    activity_level : ActivityLevelEnum

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    sex: SexEnum
    birth_date: date
    height: float
    weight: float
    activity_level: ActivityLevelEnum

    class Config:
        from_attributes = True
