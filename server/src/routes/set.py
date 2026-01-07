from fastapi import APIRouter, Depends, HTTPException
from src.types.schemas.set import SetCreate, SetRead
from src.services.set_service import SetService
from src.services.user_services import UserService
from src.core.auth.security import get_current_user

router = APIRouter(prefix="/sets", tags=["sets"])


@router.post("/exercises/{exercise_id}/sets", response_model=SetRead)
async def add_set(
    exercise_id: int,
    data: SetCreate,
    user=Depends(get_current_user),
):
    user_weight = await UserService.get_latest_weight(user.id)
    return await SetService.create(
        exercise_id=exercise_id,
        user_id=user.id,
        user_weight_kg=user_weight,
        data=data,
    )
