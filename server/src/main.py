from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from src.routes import auth, user, workout, exercise, set
from src.database.session import get_db
from src.services.health_service import HealthService
from src.types.schemas.health import HealthResponse

app = FastAPI(
    title="KiloCal API",
    description="API para acompanhamento de treinos e cálculo de calorias",
    version="1.0.0",
    openapi_prefix="/api/v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(set.router)


@app.get("/")
def root():
    return {"message": "KiloCal API is running"}


@app.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):

    return await HealthService.get_health_metrics(db)
