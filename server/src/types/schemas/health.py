from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatabaseStats(BaseModel):
    """Estatísticas do banco de dados"""

    status: str
    connection_pool_size: Optional[int] = None
    response_time_ms: Optional[float] = None


class UserStats(BaseModel):
    """Estatísticas de usuários"""

    total_users: int
    active_users_today: int
    active_users_week: int
    new_users_today: int
    new_users_week: int


class WorkoutStats(BaseModel):
    """Estatísticas de treinos"""

    total_workouts: int
    workouts_today: int
    workouts_week: int
    total_calories_burned: float
    avg_workout_duration: Optional[float] = None


class SystemStats(BaseModel):
    """Estatísticas do sistema"""

    uptime_seconds: float
    current_time: datetime
    stage: str
    api_version: str


class HealthResponse(BaseModel):
    """Resposta completa do endpoint de health"""

    status: str
    message: str
    system: SystemStats
    database: DatabaseStats
    users: UserStats
    workouts: WorkoutStats
