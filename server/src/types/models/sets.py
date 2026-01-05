from tortoise import Model, fields
from enum import Enum

class Set(Model):
    id = fields.UUIDField(pk=True)
    exercise = fields.ForeignKeyField("models.Exercisse", related_name="sets", on_delete=fields.CASCADE)
    reps = fields.IntField(null=True)
    weight = fields.FloatField(null=True)  # in kg
    duration = fields.IntField(null=True)  # in seconds
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "sets"