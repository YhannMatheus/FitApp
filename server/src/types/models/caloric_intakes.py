from tortoise import fields, Model


class CaloricIntake(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="caloric_intakes", on_delete=fields.CASCADE)
    date = fields.DateField()
    calories_consumed = fields.FloatField(default=0.0)
    protein_grams = fields.FloatField(default=0.0)
    carbs_grams = fields.FloatField(default=0.0)
    fats_grams = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "caloric_intakes"