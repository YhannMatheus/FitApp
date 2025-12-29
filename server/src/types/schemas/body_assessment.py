from datetime import date
from pydantic import BaseModel


class BodyAssessmentCreate(BaseModel):
    date: date
    weight_kg: float

    waist_cm: float | None = None
    hip_cm: float | None = None
    chest_cm: float | None = None
    arm_cm: float | None = None
    thigh_cm: float | None = None
    calf_cm: float | None = None


class BodyAssessmentResponseSchema(BaseModel):
    weight_kg: float
    body_fat_percent: float | None
    tmb: float
    tdee: float
    created_at: date

    class Config:
        from_attributes = True
