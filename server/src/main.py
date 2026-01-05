from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, user, workout, exercise, set
from server.src.core.database.connection import configure_database
from src.core.config import settings

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

database = configure_database(app, database_url=settings.DATABASE_URL)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(set.router)


@app.get("/")
def root():
    return {"message": "KiloCal API is running"}

