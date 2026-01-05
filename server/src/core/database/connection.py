from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

async def configure_database(app: FastAPI, database_url: str):
    register_tortoise(
        app,
        db_url=database_url,
        generate_schemas=True,
        add_exception_handlers=True,
    )