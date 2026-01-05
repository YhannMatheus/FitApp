from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.types.schemas.exercise import ExerciseCreate, ExerciseSchema
from src.services.exercise_service import ExerciseService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user
from src.database.session import get_db

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/workouts/{workout_id}/exercises", response_model=ExerciseSchema)
async def add_exercise(
    workout_id: int,
    data: ExerciseCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_weight = await UserService.get_latest_weight(db, user.id)
    return await ExerciseService.create(
        db=db,
        workout_id=workout_id,
        user_id=user.id,
        user_weight_kg=user_weight,
        data=data,
    )
