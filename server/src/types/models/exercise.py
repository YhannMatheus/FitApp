from tortoise import fields, Model
from src.types.enums.exercise import ExerciseTypeEnum, IntensityLevelEnum, ExercisseNameEnum

class Exercisse(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharEnumField(ExercisseNameEnum)
    workout = fields.ForeignKeyField("models.Workout", related_name="exercises", on_delete=fields.CASCADE)
    type = fields.CharEnumField(ExerciseTypeEnum)
    intensity = fields.CharEnumField(IntensityLevelEnum)
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "exercises"
