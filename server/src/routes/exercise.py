from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.types.schemas.exercise import ExerciseCreate, ExerciseSchema
from src.services.exercise_service import ExerciseService
from src.core.auth.security import get_current_user
from src.database.session import get_db

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/workouts/{workout_id}/exercises", response_model=ExerciseSchema)
async def add_exercise(
    workout_id: UUID,
    data: ExerciseCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ExerciseService.create(
        db=db,
        workout_id=workout_id,
        user_id=user.id,
        user_weight_kg=user.weight,
        data=data,
    )
