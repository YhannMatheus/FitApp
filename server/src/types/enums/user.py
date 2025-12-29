from enum import Enum


class SexEnum(str, Enum):
    male = "male"
    female = "female"


class ActivityLevelEnum(str, Enum):
    sedentary = "sedentary"
    lightly_active = "lightly_active"
    moderately_active = "moderately_active"
    very_active = "very_active"
    athlete = "athlete"
