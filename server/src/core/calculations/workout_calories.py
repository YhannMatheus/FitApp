from src.types.enums.workout import ExerciseTypeEnum, IntensityLevelEnum
from typing import Optional


class WorkoutCalories:
    MET_VALUES = {
        ExerciseTypeEnum.cardio: {
            IntensityLevelEnum.low: 3.5,
            IntensityLevelEnum.moderate: 5.0,
            IntensityLevelEnum.high: 8.0,
            IntensityLevelEnum.very_high: 11.0,
        },
        ExerciseTypeEnum.strength: {
            IntensityLevelEnum.low: 3.0,
            IntensityLevelEnum.moderate: 5.0,
            IntensityLevelEnum.high: 6.0,
            IntensityLevelEnum.very_high: 8.0,
        },
        ExerciseTypeEnum.flexibility: {
            IntensityLevelEnum.low: 2.0,
            IntensityLevelEnum.moderate: 2.5,
            IntensityLevelEnum.high: 3.0,
            IntensityLevelEnum.very_high: 4.0,
        },
        ExerciseTypeEnum.sports: {
            IntensityLevelEnum.low: 4.0,
            IntensityLevelEnum.moderate: 6.0,
            IntensityLevelEnum.high: 8.0,
            IntensityLevelEnum.very_high: 10.0,
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

        intensity = IntensityLevelEnum.moderate
        if weight_lifted_kg:
            if weight_lifted_kg > weight_kg * 0.5:
                intensity = IntensityLevelEnum.high
            elif weight_lifted_kg > weight_kg * 0.8:
                intensity = IntensityLevelEnum.very_high

        return WorkoutCalories.calculate_exercise_calories(
            ExerciseTypeEnum.strength, intensity, weight_kg, total_time_seconds
        )
