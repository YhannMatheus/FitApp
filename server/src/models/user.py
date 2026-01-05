from tortoise import Model, fields
from enum import Enum
from uuid import uuid4

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"

class ActivityLevelEnum(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    birth_date = fields.DateField()
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)

    height_cm = fields.FloatField(default=0.0)
    goal = fields.FloatField(null=True)

    gender = fields.CharEnumField(GenderEnum)
    activity_level = fields.CharEnumField(ActivityLevelEnum)
    
    activates_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"