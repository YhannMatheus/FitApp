from src.core.config import settings
from urllib.parse import urlparse, parse_qs, urlunparse

def get_tortoise_url(url: str):
    # 1. Corrige o protocolo para 'postgres'
    url = url.replace("postgresql://", "postgres://")
    
    # 2. Remove parâmetros que o asyncpg não entende (como sslmode)
    parsed = urlparse(url)
    # Retornamos a URL sem a parte da query (?sslmode=...)
    return urlunparse(parsed._replace(query=""))

database_url = get_tortoise_url(settings.DATABASE_URL)

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": urlparse(database_url).path[1:],
                "host": urlparse(database_url).hostname,
                "password": urlparse(database_url).password,
                "user": urlparse(database_url).username,
                "port": urlparse(database_url).port or 5432,
                "ssl": True,
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                "src.types.models.user", 
                "src.types.models.workout", 
                "src.types.models.exercise", 
                "src.types.models.sets", 
                "src.types.models.body_assessments",
                "src.types.models.caloric_intakes",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}