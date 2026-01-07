from typing import Dict, Optional
from src.types.enums.user import GenderEnum

class Bioimpedance:
    @staticmethod
    def calculate_body_water(lean_mass_kg: float) -> float:
        return round(lean_mass_kg * 0.73, 2)

    @staticmethod
    def calculate_ideal_weight_robinson(sex: GenderEnum, height_cm: float) -> float:
        height_inches = height_cm / 2.54

        if sex == GenderEnum.MALE:
            ideal_weight_lbs = 52 + 1.9 * (height_inches - 60)
        else:
            ideal_weight_lbs = 49 + 1.7 * (height_inches - 60)

        ideal_weight_kg = ideal_weight_lbs * 0.453592
        return round(max(40, ideal_weight_kg), 2)

    @staticmethod
    def calculate_waist_to_hip_ratio(waist_cm: float, hip_cm: float) -> float:
        return round(waist_cm / hip_cm, 2)

    @staticmethod
    def classify_waist_to_hip_ratio(ratio: float, sex: GenderEnum) -> str:
        if sex == GenderEnum.MALE:
            if ratio < 0.90:
                return "Baixo risco"
            elif ratio < 1.0:
                return "Risco moderado"
            else:
                return "Risco alto"
        else:
            if ratio < 0.80:
                return "Baixo risco"
            elif ratio < 0.85:
                return "Risco moderado"
            else:
                return "Risco alto"

    @staticmethod
    def calculate_body_composition(
        weight_kg: float,
        body_fat_percentage: float,
        lean_mass_kg: Optional[float] = None,
    ) -> Dict[str, float]:
        fat_mass = weight_kg * (body_fat_percentage / 100)

        if lean_mass_kg is None:
            lean_mass = weight_kg - fat_mass
        else:
            lean_mass = lean_mass_kg

        body_water = lean_mass * 0.73

        return {
            "weight_kg": round(weight_kg, 2),
            "fat_mass_kg": round(fat_mass, 2),
            "lean_mass_kg": round(lean_mass, 2),
            "body_water_kg": round(body_water, 2),
            "body_fat_percentage": round(body_fat_percentage, 2),
            "lean_mass_percentage": round((lean_mass / weight_kg) * 100, 2),
        }
