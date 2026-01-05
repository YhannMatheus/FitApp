from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.types.models_old.user import User
from src.types.models_old.workout import Workout
from src.types.schemas.health import (
    HealthResponse,
    SystemStats,
    DatabaseStats,
    UserStats,
    WorkoutStats,
)
from src.core.config import settings
import time


class HealthService:
    _start_time = time.time()

    @staticmethod
    async def get_health_metrics(db: AsyncSession) -> HealthResponse:
        """Coleta e retorna todas as métricas de saúde da aplicação"""

        # System Stats
        uptime = time.time() - HealthService._start_time
        system_stats = SystemStats(
            uptime_seconds=round(uptime, 2),
            current_time=datetime.utcnow(),
            stage=settings.STAGE,
            api_version="1.0.0",
        )

        # Database Stats
        db_stats = await HealthService._get_database_stats(db)

        # User Stats
        user_stats = await HealthService._get_user_stats(db)

        # Workout Stats
        workout_stats = await HealthService._get_workout_stats(db)

        status = "healthy" if db_stats.status == "connected" else "degraded"

        return HealthResponse(
            status=status,
            message=(
                "API está operacional"
                if status == "healthy"
                else "API com problemas de conexão"
            ),
            system=system_stats,
            database=db_stats,
            users=user_stats,
            workouts=workout_stats,
        )

    @staticmethod
    async def _get_database_stats(db: AsyncSession) -> DatabaseStats:
        """Coleta estatísticas do banco de dados"""
        try:
            start = time.time()
            await db.execute(select(1))
            response_time = (time.time() - start) * 1000  # Convert to ms

            # Get pool size if available
            pool_size = None
            try:
                # Tenta acessar o pool do engine
                engine = db.get_bind()
                if hasattr(engine, "pool"):
                    pool = engine.pool  # type: ignore
                    if hasattr(pool, "size"):
                        pool_size = pool.size()  # type: ignore
            except Exception:
                # Se não conseguir acessar o pool, mantém None
                pass

            return DatabaseStats(
                status="connected",
                connection_pool_size=pool_size,
                response_time_ms=round(response_time, 2),
            )
        except Exception as e:
            return DatabaseStats(
                status="disconnected", connection_pool_size=None, response_time_ms=None
            )

    @staticmethod
    async def _get_user_stats(db: AsyncSession) -> UserStats:
        """Coleta estatísticas de usuários"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = today_start - timedelta(days=7)

        # Total de usuários
        total_users_result = await db.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar() or 0

        # Novos usuários hoje
        new_users_today_result = await db.execute(
            select(func.count(User.id)).where(User.created_at >= today_start)
        )
        new_users_today = new_users_today_result.scalar() or 0

        # Novos usuários esta semana
        new_users_week_result = await db.execute(
            select(func.count(User.id)).where(User.created_at >= week_start)
        )
        new_users_week = new_users_week_result.scalar() or 0

        # Usuários ativos hoje (que criaram treino hoje)
        active_today_result = await db.execute(
            select(func.count(func.distinct(Workout.user_id))).where(
                Workout.created_at >= today_start
            )
        )
        active_today = active_today_result.scalar() or 0

        # Usuários ativos esta semana
        active_week_result = await db.execute(
            select(func.count(func.distinct(Workout.user_id))).where(
                Workout.created_at >= week_start
            )
        )
        active_week = active_week_result.scalar() or 0

        return UserStats(
            total_users=total_users,
            active_users_today=active_today,
            active_users_week=active_week,
            new_users_today=new_users_today,
            new_users_week=new_users_week,
        )

    @staticmethod
    async def _get_workout_stats(db: AsyncSession) -> WorkoutStats:
        """Coleta estatísticas de treinos"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = today_start - timedelta(days=7)

        # Total de treinos
        total_workouts_result = await db.execute(select(func.count(Workout.id)))
        total_workouts = total_workouts_result.scalar() or 0

        # Treinos hoje
        workouts_today_result = await db.execute(
            select(func.count(Workout.id)).where(Workout.created_at >= today_start)
        )
        workouts_today = workouts_today_result.scalar() or 0

        # Treinos esta semana
        workouts_week_result = await db.execute(
            select(func.count(Workout.id)).where(Workout.created_at >= week_start)
        )
        workouts_week = workouts_week_result.scalar() or 0

        # Total de calorias queimadas
        total_calories_result = await db.execute(
            select(func.sum(Workout.total_calories_burned))
        )
        total_calories = total_calories_result.scalar() or 0.0

        return WorkoutStats(
            total_workouts=total_workouts,
            workouts_today=workouts_today,
            workouts_week=workouts_week,
            total_calories_burned=round(total_calories, 2),
            avg_workout_duration=None,  # Pode ser implementado se houver campo de duração
        )
