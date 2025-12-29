from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from src.types.models.set import Set
from src.types.models.exercise import Exercise
from src.types.models.workout import Workout
from src.types.schemas.set import SetCreate, SetUpdate
from src.core.calculations.workout_calories import WorkoutCalories


class SetService:
    @staticmethod
    async def create(
        db: AsyncSession,
        exercise_id: UUID,
        user_id: UUID,
        user_weight_kg: float,
        data: SetCreate,
    ) -> Set:
        exercise_result = await db.execute(
            select(Exercise)
            .join(Workout)
            .where(Exercise.id == exercise_id, Workout.user_id == user_id)
        )
        exercise = exercise_result.scalar_one_or_none()

        if not exercise:
            raise ValueError("Exercise not found or does not belong to user")

        if data.duration:
            set_calories = WorkoutCalories.calculate_exercise_calories(
                exercise.exercise_type,
                exercise.intensity,
                user_weight_kg,
                data.duration,
            )
        elif data.reps and data.weight:
            set_calories = WorkoutCalories.calculate_strength_calories(
                user_weight_kg, 1, data.reps, data.weight
            )
        else:
            set_calories = 0.0

        set_obj = Set(
            exercise_id=exercise_id,
            reps=data.reps,
            weight=data.weight,
            duration=data.duration,
            calories_burned=set_calories,
        )
        db.add(set_obj)
        await db.flush()

        exercise.calories_burned = (exercise.calories_burned or 0.0) + set_calories

        workout_result = await db.execute(
            select(Workout).where(Workout.id == exercise.workout_id)
        )
        workout = workout_result.scalar_one()
        workout.total_calories_burned = (
            workout.total_calories_burned or 0.0
        ) + set_calories

        await db.commit()
        await db.refresh(set_obj)

        return set_obj

    @staticmethod
    async def get_by_id(db: AsyncSession, set_id: UUID, user_id: UUID) -> Optional[Set]:
        result = await db.execute(
            select(Set)
            .join(Exercise)
            .join(Workout)
            .where(Set.id == set_id, Workout.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_exercise(
        db: AsyncSession, exercise_id: UUID, user_id: UUID
    ) -> List[Set]:
        result = await db.execute(
            select(Set)
            .join(Exercise)
            .join(Workout)
            .where(Set.exercise_id == exercise_id, Workout.user_id == user_id)
            .order_by(Set.created_at)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        set_id: UUID,
        user_id: UUID,
        user_weight_kg: float,
        data: SetUpdate,
    ) -> Optional[Set]:
        set_obj = await SetService.get_by_id(db, set_id, user_id)

        if not set_obj:
            return None

        exercise_result = await db.execute(
            select(Exercise).where(Exercise.id == set_obj.exercise_id)
        )
        exercise = exercise_result.scalar_one()

        old_set_calories = set_obj.calories_burned or 0.0

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(set_obj, key, value)

        if set_obj.duration:
            new_set_calories = WorkoutCalories.calculate_exercise_calories(
                exercise.exercise_type,
                exercise.intensity,
                user_weight_kg,
                set_obj.duration,
            )
        elif set_obj.reps and set_obj.weight:
            new_set_calories = WorkoutCalories.calculate_strength_calories(
                user_weight_kg, 1, set_obj.reps, set_obj.weight
            )
        else:
            new_set_calories = 0.0

        set_obj.calories_burned = new_set_calories
        calories_diff = new_set_calories - old_set_calories

        exercise.calories_burned = (exercise.calories_burned or 0.0) + calories_diff

        workout_result = await db.execute(
            select(Workout).where(Workout.id == exercise.workout_id)
        )
        workout = workout_result.scalar_one()
        workout.total_calories_burned = (
            workout.total_calories_burned or 0.0
        ) + calories_diff

        await db.commit()
        await db.refresh(set_obj)

        return set_obj

    @staticmethod
    async def delete(db: AsyncSession, set_id: UUID, user_id: UUID) -> bool:
        set_obj = await SetService.get_by_id(db, set_id, user_id)

        if not set_obj:
            return False

        exercise_result = await db.execute(
            select(Exercise).where(Exercise.id == set_obj.exercise_id)
        )
        exercise = exercise_result.scalar_one()

        set_calories = set_obj.calories_burned or 0.0

        exercise.calories_burned = (exercise.calories_burned or 0.0) - set_calories

        workout_result = await db.execute(
            select(Workout).where(Workout.id == exercise.workout_id)
        )
        workout = workout_result.scalar_one()
        workout.total_calories_burned = (
            workout.total_calories_burned or 0.0
        ) - set_calories

        await db.delete(set_obj)
        await db.commit()

        return True
