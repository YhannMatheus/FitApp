from tortoise import fields, Model
from uuid import uuid4
from src.types.enums.workout import TrainingTypeEnum

class Workout(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="workouts", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)

    type = fields.CharEnumField(TrainingTypeEnum)
    total_calories_burned = fields.FloatField(default=0.0)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)

    create_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "workouts"

    @property
    def duration_minutes(self) -> float:
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60.0
        return 0.0