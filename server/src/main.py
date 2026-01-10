from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import user
from src.core.database.connection import configure_database
from src.core.middlewares.auth_middleware import AuthMiddleware

app = FastAPI(
    title="KiloCal API",
    description="API para acompanhamento de treinos e cálculo de calorias",
    version="1.0.0",
    openapi_prefix="/api/v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://kilocal-8fy9.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

database = configure_database(app)

app.include_router(user.router)
#app.include_router(workout.router)
#app.include_router(exercise.router)
#app.include_router(set.router)


@app.get("/")
def root():
    return {"message": "KiloCal API is running"}

