from enum import Enum


class ExerciseTypeEnum(str, Enum):
    cardio = "cardio"
    strength = "strength"
    flexibility = "flexibility"
    sports = "sports"


class ExerciseCategoryEnum(str, Enum):
    upper_body = "upper_body"
    lower_body = "lower_body"
    full_body = "full_body"
    core = "core"
    cardio = "cardio"


class IntensityLevelEnum(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    very_high = "very_high"
