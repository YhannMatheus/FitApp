from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from src.types.models.workout import Workout
from src.types.models.exercise import Exercise
from src.types.models.set import Set
from src.types.schemas.workout import (
    WorkoutCreate,
    WorkoutUpdate,
    WorkoutSchema,
    WorkoutSummarySchema,
)
from src.core.calculations.workout_calories import WorkoutCalories


class WorkoutService:
    @staticmethod
    async def create(
        db: AsyncSession, user_id: UUID, user_weight_kg: float, data: WorkoutCreate
    ) -> Workout:
        workout = Workout(
            user_id=user_id,
            name=data.name,
            description=data.description,
            total_calories_burned=0.0,
        )
        db.add(workout)
        await db.flush()

        total_calories = 0.0

        for exercise_data in data.exercises:
            exercise = Exercise(
                workout_id=workout.id,
                name=exercise_data.name,
                description=exercise_data.description,
                exercise_type=exercise_data.exercise_type,
                category=exercise_data.category,
                intensity=exercise_data.intensity,
                calories_burned=0.0,
            )
            db.add(exercise)
            await db.flush()

            exercise_calories = 0.0

            for set_data in exercise_data.sets:
                if set_data.duration:
                    set_calories = WorkoutCalories.calculate_exercise_calories(
                        exercise_data.exercise_type,
                        exercise_data.intensity,
                        user_weight_kg,
                        set_data.duration,
                    )
                elif set_data.reps and set_data.weight:
                    set_calories = WorkoutCalories.calculate_strength_calories(
                        user_weight_kg, 1, set_data.reps, set_data.weight
                    )
                else:
                    set_calories = 0.0

                set_obj = Set(
                    exercise_id=exercise.id,
                    reps=set_data.reps,
                    weight=set_data.weight,
                    duration=set_data.duration,
                    calories_burned=set_calories,
                )
                db.add(set_obj)

                exercise_calories += set_calories

            exercise.calories_burned = round(exercise_calories, 2)
            total_calories += exercise_calories

        workout.total_calories_burned = round(total_calories, 2)

        await db.refresh(workout)

        return workout

    @staticmethod
    async def get_by_id(
        db: AsyncSession, workout_id: UUID, user_id: UUID
    ) -> Optional[Workout]:
        result = await db.execute(
            select(Workout)
            .options(selectinload(Workout.exercises).selectinload(Exercise.sets))
            .where(Workout.id == workout_id, Workout.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Workout]:
        result = await db.execute(
            select(Workout)
            .where(Workout.user_id == user_id)
            .order_by(Workout.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_date_range(
        db: AsyncSession, user_id: UUID, start_date: date, end_date: date
    ) -> List[Workout]:
        result = await db.execute(
            select(Workout)
            .where(
                Workout.user_id == user_id,
                func.date(Workout.created_at) >= start_date,
                func.date(Workout.created_at) <= end_date,
            )
            .order_by(Workout.created_at.desc())
        )
        return list(result.scalars().all())
