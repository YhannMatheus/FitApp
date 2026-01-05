from tortoise import Model, fields
from enum import Enum

class BodyAssessment(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="body_assessments", on_delete=fields.CASCADE)
    
    # --- MEDIDAS BÁSICAS ---
    weight_kg = fields.FloatField(description="Peso total no dia da avaliação")
    height_cm = fields.FloatField(description="Altura no momento (importante para crianças/jovens)")

    # --- CIRCUNFERÊNCIAS ---
    waist_cm = fields.FloatField(null=True)
    hip_cm = fields.FloatField(null=True)
    chest_cm = fields.FloatField(null=True)
    neck_cm = fields.FloatField(null=True)
    arm_cm = fields.FloatField(null=True)
    thigh_cm = fields.FloatField(null=True)

    # --- DOBRAS CUTÂNEAS ---
    fold_chest = fields.FloatField(null=True)      # Peitoral
    fold_abdominal = fields.FloatField(null=True)  # Abdominal
    fold_thigh = fields.FloatField(null=True)      # Coxa
    fold_triceps = fields.FloatField(null=True)    # Tríceps
    fold_subscapular = fields.FloatField(null=True) # Subescapular
    fold_suprailiac = fields.FloatField(null=True) # Supra-ilíaca
    fold_midaxillary = fields.FloatField(null=True) # Axilar média

    # --- RESULTADOS CALCULADOS ---
    bfp = fields.FloatField(null=True)           # % de Gordura
    bmi = fields.FloatField(null=True)           # IMC
    bmr = fields.FloatField(null=True)           # Taxa Metabólica Basal
    tdee = fields.FloatField(null=True)          # Gasto Calórico Total
    lean_mass_kg = fields.FloatField(null=True)  # Massa Magra
    fat_mass_kg = fields.FloatField(null=True)   # Massa Gorda

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "body_assessments"