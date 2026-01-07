from src.types.models.sets import Set
from src.types.schemas.set import SetCreate, SetUpdate, SetRead
from fastapi import HTTPException, status
from uuid import UUID

class SetService:
    @staticmethod
    async def create(exercise_id: UUID, user_id: UUID, user_weight_kg: float, data: SetCreate) -> Set:
        try:
            set_instance = await Set.create(
                exercise_id=exercise_id,
                reps=data.reps,
                weight=data.weight,
                duration=data.duration
            )
            if not set_instance:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create set"
                )
            return set_instance
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating set: {str(e)}"
            )
    
    @staticmethod
    async def get_by_id(set_id: UUID) -> Set:
        set_instance = await Set.get_or_none(id=set_id)
        if not set_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Set not found"
            )
        return set_instance
    
    @staticmethod
    async def update(set_id: UUID, data: SetUpdate) -> Set:
        set_instance = await SetService.get_by_id(set_id)
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(set_instance, field, value)
        
        await set_instance.save()
        return set_instance
    
    @staticmethod
    async def delete(set_id: UUID) -> None:
        set_instance = await SetService.get_by_id(set_id)
        await set_instance.delete()
