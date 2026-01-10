from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from src.types.schemas.user import UserRead

class BodyAssessmentBase(BaseModel):
    id : UUID
    user_id: UUID
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

class BodyAssessmentReed(BaseModel):
    id : UUID
    bfp: Optional[float] = Field(None, description="% de Gordura")
    bmi: Optional[float] = Field(None, description="IMC")
    bmr: Optional[float] = Field(None, description="Taxa Metabólica Basal")
    tdee: Optional[float] = Field(None, description="Gasto Calórico Total")
    lean_mass_kg: Optional[float] = Field(None, description="Massa Magra")
    fat_mass_kg: Optional[float] = Field(None, description="Massa Gorda")
    created_at: datetime

class BodyAssessmentCreate(BaseModel):
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

class WeigthGraphPoint(BaseModel):
    date: datetime
    weight_kg: float

class BFPGraphPoint(BaseModel):
    date: datetime
    bfp: float

class BMIGraphPoint(BaseModel):
    date: datetime
    bmi: float

class BMRGraphPoint(BaseModel):
    date: datetime
    bmr: float

class TDEEGraphPoint(BaseModel):
    date: datetime
    tdee: float

class LFMassGraphPoint(BaseModel):
    date: datetime
    lean_mass_kg: float
    fat_mass_kg: float

class BodyAssessmentGraphs(BaseModel):
    bfp_graph: list[BFPGraphPoint]
    bmi_graph: list[BMIGraphPoint]
    tdee_graph: list[TDEEGraphPoint]
    lf_mass_graph: list[LFMassGraphPoint]
    weight_graph: list[WeigthGraphPoint]