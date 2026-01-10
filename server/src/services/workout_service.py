from src.types.models.workout import Workout
from src.types.schemas.workout import *
from fastapi import HTTPException, status
from datetime import date

class WorkoutService:
    @staticmethod
    async def create_workout(data : WorkoutCreate) -> Workout:
        try:
            workout = await Workout.create(**data.dict())
            if not workout:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create workout"
                )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating workout: {str(e)}"
            )
        
        return workout
    
    @staticmethod
    async def get_user_workouts(user_id: str) -> list[Workout]:
        try:
            workouts = await Workout.filter(user_id=user_id).all()
            if workouts is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No workouts found for the user"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workouts: {str(e)}"
            )
        
        return workouts
    
    @staticmethod
    async def get_workout_by_id(workout_id: str) -> Workout:
        try:
            workout = await Workout.get_or_none(id=workout_id)
            if workout is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout not found"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workout: {str(e)}"
            )
        
        return workout