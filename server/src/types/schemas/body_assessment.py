from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class BodyAssessmentBase(BaseModel):
    id : UUID
    weight_kg: float = Field(..., gt=0, description="Peso total no dia da avaliação")
    height_cm: float = Field(..., gt=0, description="Altura no momento")
    waist_cm: Optional[float] = Field(None, gt=0)
    hip_cm: Optional[float] = Field(None, gt=0)
    chest_cm: Optional[float] = Field(None, gt=0)
    neck_cm: Optional[float] = Field(None, gt=0)
    arm_cm: Optional[float] = Field(None, gt=0)
    thigh_cm: Optional[float] = Field(None, gt=0)
    
    fold_chest: Optional[float] = Field(None, ge=0)
    fold_abdominal: Optional[float] = Field(None, ge=0)
    fold_thigh: Optional[float] = Field(None, ge=0)
    fold_triceps: Optional[float] = Field(None, ge=0)
    fold_subscapular: Optional[float] = Field(None, ge=0)
    fold_suprailiac: Optional[float] = Field(None, ge=0)
    fold_midaxillary: Optional[float] = Field(None, ge=0)

    bfp: Optional[float] = Field(None, description="% de Gordura")
    bmi: Optional[float] = Field(None, description="IMC")
    bmr: Optional[float] = Field(None, description="Taxa Metabólica Basal")
    tdee: Optional[float] = Field(None, description="Gasto Calórico Total")
    lean_mass_kg: Optional[float] = Field(None, description="Massa Magra")
    fat_mass_kg: Optional[float] = Field(None, description="Massa Gorda")
    created_at: datetime