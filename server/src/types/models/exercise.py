from tortoise import fields, Model
from enum import Enum

class ExerciseTypeEnum(str, Enum):
    BACK = "back"
    CHEST = "chest"
    LEGS = "legs"
    ARMS = "arms"
    SHOULDERS = "shoulders"
    ABDOMEN = "abdomen"

class IntensityLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class Exercisse(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    workout = fields.ForeignKeyField("models.Workout", related_name="exercises", on_delete=fields.CASCADE)
    type = fields.CharEnumField(ExerciseTypeEnum)
    intensity = fields.CharEnumField(IntensityLevelEnum)
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "exercises"
