from fastapi import APIRouter, Depends, HTTPException
from src.types.schemas.exercise import ExerciseCreate, ExerciseRead
from src.services.exercise_service import ExerciseService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/workouts/{workout_id}/exercises", response_model=ExerciseRead)
async def add_exercise(
    workout_id: int,
    data: ExerciseCreate,
    user=Depends(get_current_user),
):
    user_weight = await UserService.get_latest_weight(user.id)
    return await ExerciseService.create(
        workout_id=workout_id,
        user_id=user.id,
        user_weight_kg=user_weight,
        data=data,
    )
