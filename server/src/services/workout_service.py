from src.types.models.workout import Workout
from src.types.schemas.workout import *
from fastapi import HTTPException, status
from datetime import date

class WorkoutService:
    @staticmethod
    async def create_workout(data : WorkoutBase) -> Workout:
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
    async def get_workout_by_id(workout_id: str) -> Workout:
        workout = await Workout.get_or_none(id=workout_id).prefetch_related("exercises")
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workout not found"
            )
        return workout
    
    @staticmethod
    async def complete_workout(workout_id: str, data: WorkoutComplete) -> Workout:
        workout = await WorkoutService.get_workout_by_id(workout_id)
        workout.end_time = data.end_time
        await workout.save()
        return workout
    
    @staticmethod
    async def update_workout(workout_id: str, data: WorkoutUpdate) -> Workout:
        workout = await WorkoutService.get_workout_by_id(workout_id)
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(workout, field, value)
        
        await workout.save()
        return workout
    
    @staticmethod
    async def delete_workout(workout_id: str) -> None:
        workout = await WorkoutService.get_workout_by_id(workout_id)
        await workout.delete()

    @staticmethod
    async def List_workouts_days(user_id: str) -> list[date]:
        workouts = await Workout.filter(user_id=user_id).distinct().order_by('start_time')
        workout_days = sorted({workout.start_time.date() for workout in workouts})
        return workout_days
    
    @staticmethod
    async def list_workouts_calories(user_id: str, workout_date: date) -> list[float]:
        workouts = await Workout.filter(
            user_id=user_id,
            start_time__date=workout_date
        ).order_by('start_time')
        calories_list = [workout.total_calories_burned for workout in workouts]
        return calories_list
    
    @staticmethod
    async def list_workouts_by_date(user_id: str, workout_date: date) -> list[Workout]:
        workouts = await Workout.filter(
            user_id=user_id,
            start_time__date=workout_date
        ).order_by('start_time')
        return workouts