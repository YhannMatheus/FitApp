from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from src.types.models.exercise import Exercise
from src.types.models.set import Set
from src.types.models.workout import Workout
from src.types.schemas.exercise import ExerciseCreate, ExerciseUpdate
from src.core.calculations.workout_calories import WorkoutCalories


class ExerciseService:
    @staticmethod
    async def create(
        db: AsyncSession,
        workout_id: UUID,
        user_id: UUID,
        user_weight_kg: float,
        data: ExerciseCreate,
    ) -> Exercise:
        workout_result = await db.execute(
            select(Workout).where(Workout.id == workout_id, Workout.user_id == user_id)
        )
        workout = workout_result.scalar_one_or_none()

        if not workout:
            raise ValueError("Workout not found or does not belong to user")

        exercise = Exercise(
            workout_id=workout_id,
            name=data.name,
            description=data.description,
            exercise_type=data.exercise_type,
            category=data.category,
            intensity=data.intensity,
            calories_burned=0.0,
        )
        db.add(exercise)
        await db.flush()

        exercise_calories = 0.0

        for set_data in data.sets:
            if set_data.duration:
                set_calories = WorkoutCalories.calculate_exercise_calories(
                    data.exercise_type,
                    data.intensity,
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
        workout.total_calories_burned = (
            workout.total_calories_burned or 0.0
        ) + exercise_calories

        await db.commit()
        await db.refresh(exercise)

        return exercise

    @staticmethod
    async def get_by_id(
        db: AsyncSession, exercise_id: UUID, user_id: UUID
    ) -> Optional[Exercise]:
        result = await db.execute(
            select(Exercise)
            .join(Workout)
            .options(selectinload(Exercise.sets))
            .where(Exercise.id == exercise_id, Workout.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_workout(
        db: AsyncSession, workout_id: UUID, user_id: UUID
    ) -> List[Exercise]:
        result = await db.execute(
            select(Exercise)
            .join(Workout)
            .options(selectinload(Exercise.sets))
            .where(Exercise.workout_id == workout_id, Workout.user_id == user_id)
            .order_by(Exercise.created_at)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        exercise_id: UUID,
        user_id: UUID,
        user_weight_kg: float,
        data: ExerciseUpdate,
    ) -> Optional[Exercise]:
        exercise = await ExerciseService.get_by_id(db, exercise_id, user_id)

        if not exercise:
            return None

        old_calories = await ExerciseService._calculate_exercise_calories(
            exercise, user_weight_kg
        )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(exercise, key, value)

        new_calories = await ExerciseService._calculate_exercise_calories(
            exercise, user_weight_kg
        )

        workout_result = await db.execute(
            select(Workout).where(Workout.id == exercise.workout_id)
        )
        workout = workout_result.scalar_one()
        workout.total_calories_burned = (
            (workout.total_calories_burned or 0.0) - old_calories + new_calories
        )

        await db.commit()
        await db.refresh(exercise)

        return exercise

    @staticmethod
    async def delete(
        db: AsyncSession, exercise_id: UUID, user_id: UUID, user_weight_kg: float
    ) -> bool:
        exercise = await ExerciseService.get_by_id(db, exercise_id, user_id)

        if not exercise:
            return False

        exercise_calories = await ExerciseService._calculate_exercise_calories(
            exercise, user_weight_kg
        )

        workout_result = await db.execute(
            select(Workout).where(Workout.id == exercise.workout_id)
        )
        workout = workout_result.scalar_one()
        workout.total_calories_burned = max(
            0.0, (workout.total_calories_burned or 0.0) - exercise_calories
        )

        await db.delete(exercise)
        await db.commit()

        return True

    @staticmethod
    async def _calculate_exercise_calories(
        exercise: Exercise, user_weight_kg: float
    ) -> float:
        return sum(set_obj.calories_burned or 0.0 for set_obj in exercise.sets)
