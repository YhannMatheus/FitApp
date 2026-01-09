from src.types.enums.user import GenderEnum, ActivityLevelEnum
from src.types.enums.calculations import BMRFormulaEnum


class EnergyExpenditure:
    ACTIVITY_MULTIPLIERS = {
        ActivityLevelEnum.SEDENTARY: 1.2,
        ActivityLevelEnum.LIGHTLY_ACTIVE: 1.375,
        ActivityLevelEnum.MODERATELY_ACTIVE: 1.55,
        ActivityLevelEnum.VERY_ACTIVE: 1.725,
        ActivityLevelEnum.ATHLETE: 1.9,
    }

    @staticmethod
    def calculate_bmr_harris_benedict(
        sex: GenderEnum, weight_kg: float, height_cm: float, age: int
    ) -> float:
        if sex == GenderEnum.MALE:
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

        return round(bmr, 2)

    @staticmethod
    def calculate_bmr_mifflin(
        sex: GenderEnum, weight_kg: float, height_cm: float, age: int
    ) -> float:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)

        if sex == GenderEnum.MALE:
            bmr += 5
        else:
            bmr -= 161

        return round(bmr, 2)

    @staticmethod
    def calculate_bmr(
        sex: GenderEnum,
        weight_kg: float,
        height_cm: float,
        age: int,
        formula: BMRFormulaEnum = BMRFormulaEnum.MIFFLIN_ST_JEOR,
    ) -> float:
        if formula == BMRFormulaEnum.HARRIS_BENEDICT:
            return EnergyExpenditure.calculate_bmr_harris_benedict(
                sex, weight_kg, height_cm, age
            )
        else:
            return EnergyExpenditure.calculate_bmr_mifflin(
                sex, weight_kg, height_cm, age
            )

    @staticmethod
    def calculate_tdee(bmr: float, activity_level: ActivityLevelEnum) -> float:
        multiplier = EnergyExpenditure.ACTIVITY_MULTIPLIERS[activity_level]
        return round(bmr * multiplier, 2)

    @staticmethod
    def calculate_caloric_balance(
        calories_consumed: float, calories_burned: float, tdee: float
    ) -> float:

        total_expenditure = tdee + calories_burned
        balance = calories_consumed - total_expenditure
        return round(balance, 2)
