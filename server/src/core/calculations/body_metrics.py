import math
from datetime import date
from typing import Optional
from src.types.enums.user import GenderEnum
from src.types.enums.calculations import BodyFatFormulaEnum



class BodyMetrics:
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        height_m = height_cm / 100
        return round(weight_kg / (height_m**2), 2)

    @staticmethod
    def calculate_age(birth_date: date) -> int:
        today = date.today()
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    @staticmethod
    def calculate_body_fat_navy(
        sex: GenderEnum,
        waist_cm: float,
        neck_cm: float,
        height_cm: float,
        hip_cm: Optional[float] = None,
    ) -> float:

        if sex == GenderEnum.MALE:
            body_fat = (
                495
                / (
                    1.0324
                    - 0.19077 * math.log10(waist_cm - neck_cm)
                    + 0.15456 * math.log10(height_cm)
                )
                - 450
            )
        else:
            if hip_cm is None:
                raise ValueError("Hip measurement required for females")
            body_fat = (
                495
                / (
                    1.29579
                    - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm)
                    + 0.22100 * math.log10(height_cm)
                )
                - 450
            )

        return round(max(0, body_fat), 2)

    @staticmethod
    def calculate_lean_mass(weight_kg: float, body_fat_percentage: float) -> float:
        fat_mass = weight_kg * (body_fat_percentage / 100)
        lean_mass = weight_kg - fat_mass
        return round(lean_mass, 2)

    @staticmethod
    def calculate_fat_mass(weight_kg: float, body_fat_percentage: float) -> float:
        fat_mass = weight_kg * (body_fat_percentage / 100)
        return round(fat_mass, 2)

    @staticmethod
    def classify_bmi(bmi: float) -> str:
        if bmi < 18.5:
            return "Abaixo do peso"
        elif bmi < 25:
            return "Peso normal"
        elif bmi < 30:
            return "Sobrepeso"
        elif bmi < 35:
            return "Obesidade Grau I"
        elif bmi < 40:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III"
