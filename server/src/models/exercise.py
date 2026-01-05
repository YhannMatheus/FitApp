from tortoise import fields, Model
from enum import Enum

class ExerciseTypeEnum(str, Enum):
    BACK = "back"
    CHEST = "chest"
    LEGS = "legs"
    ARMS = "arms"
    SHOULDERS = "shoulders"
    ABDOMEN = "abdomen"

class Exercisse(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    type = fields.CharEnumField(ExerciseTypeEnum)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "exercises"
