from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.types.schemas.workout import WorkoutCreate, WorkoutSchema
from src.services.workout_service import WorkoutService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user
from src.database.session import get_db
from typing import List

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutSchema)
async def create_workout(
    data: WorkoutCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_weight = await UserService.get_latest_weight(db, user.id)
    return await WorkoutService.create(
        db=db, user_id=user.id, user_weight_kg=user_weight, data=data
    )
