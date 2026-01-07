from typing import Optional
from src.types.enums.calculations import ResistanceTypeEnum
from src.types.enums.exercise import IntensityLevelEnum, ExerciseTypeEnum


class WorkoutCalories:
    MET_VALUES = {
        ExerciseTypeEnum.CARDIO: {
            IntensityLevelEnum.LOW: 3.5,
            IntensityLevelEnum.MODERATE: 5.0,
            IntensityLevelEnum.HIGH: 8.0,
            IntensityLevelEnum.VERY_HIGH: 11.0,
        },
        ExerciseTypeEnum.STRENGTH: {
            IntensityLevelEnum.LOW: 3.0,
            IntensityLevelEnum.MODERATE: 5.0,
            IntensityLevelEnum.HIGH: 6.0,
            IntensityLevelEnum.VERY_HIGH: 8.0,
        },
        ExerciseTypeEnum.FLEXIBILITY: {
            IntensityLevelEnum.LOW: 2.0,
            IntensityLevelEnum.MODERATE: 2.5,
            IntensityLevelEnum.HIGH: 3.0,
            IntensityLevelEnum.VERY_HIGH: 4.0,
        },
        ExerciseTypeEnum.SPORTS: {
            IntensityLevelEnum.LOW: 4.0,
            IntensityLevelEnum.MODERATE: 6.0,
            IntensityLevelEnum.HIGH: 8.0,
            IntensityLevelEnum.VERY_HIGH: 10.0,
        },
    }

    @staticmethod
    def calculate_calories_from_met(
        met: float, weight_kg: float, duration_minutes: float
    ) -> float:
        duration_hours = duration_minutes / 60
        calories = met * weight_kg * duration_hours
        return round(calories, 2)

    @staticmethod
    def calculate_exercise_calories(
        exercise_type: ExerciseTypeEnum,
        intensity: IntensityLevelEnum,
        weight_kg: float,
        duration_seconds: int,
    ) -> float:
        met = WorkoutCalories.MET_VALUES[exercise_type][intensity]
        duration_minutes = duration_seconds / 60

        return WorkoutCalories.calculate_calories_from_met(
            met, weight_kg, duration_minutes
        )

    @staticmethod
    def calculate_strength_calories(
        weight_kg: float,
        sets: int,
        reps: int,
        weight_lifted_kg: Optional[float] = None,
        rest_seconds: int = 60,
    ) -> float:
        work_time_seconds = sets * reps * 3
        rest_time_seconds = (sets - 1) * rest_seconds
        total_time_seconds = work_time_seconds + rest_time_seconds

        intensity = IntensityLevelEnum.MODERATE
        if weight_lifted_kg:
            if weight_lifted_kg > weight_kg * 0.5:
                intensity = IntensityLevelEnum.HIGH
            elif weight_lifted_kg > weight_kg * 0.8:
                intensity = IntensityLevelEnum.VERY_HIGH

        return WorkoutCalories.calculate_exercise_calories(
            ExerciseTypeEnum.STRENGTH, intensity, weight_kg, total_time_seconds
        )
