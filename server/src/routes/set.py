from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.types.schemas.set import SetCreate, SetSchema
from src.services.set_service import SetService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user
from src.database.session import get_db

router = APIRouter(prefix="/sets", tags=["sets"])


@router.post("/exercises/{exercise_id}/sets", response_model=SetSchema)
async def add_set(
    exercise_id: int,
    data: SetCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_weight = await UserService.get_latest_weight(db, user.id)
    return await SetService.create(
        db=db,
        exercise_id=exercise_id,
        user_id=user.id,
        user_weight_kg=user_weight,
        data=data,
    )
