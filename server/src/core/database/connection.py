from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

def configure_database(app: FastAPI, database_url: str):
    register_tortoise(
        app,
        db_url=database_url,
        modules={"models": [
            "src.types.models.user", 
            "src.types.models.workout", 
            "src.types.models.exercise", 
            "src.types.models.sets", 
            "src.types.models.body_assessments",
            "src.types.models.caloric_intakes"
            ]},
        generate_schemas=True,
        add_exception_handlers=True,
    )