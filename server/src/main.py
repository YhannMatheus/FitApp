from fastapi import FastAPI
from src.routes import auth, user, workout, exercise, set

app = FastAPI(
    title="KiloCal API",
    description="API para acompanhamento de treinos e cálculo de calorias",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(set.router)


@app.get("/")
def root():
    return {"message": "KiloCal API is running"}
