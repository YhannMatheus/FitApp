from fastapi import APIRouter, Depends, HTTPException
from src.types.schemas.workout import WorkoutCreate
from src.services.workout_service import WorkoutService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user
from typing import List

router = APIRouter(prefix="/workouts", tags=["workouts"])
