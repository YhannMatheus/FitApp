from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP
    APP_NAME: str = "KiloCal"
    ENV: str = "dev"
    DEBUG: bool = False

    # DATABASE
    DATABASE_URL: str

    # SECURITY
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
        )


settings = Settings() #type: ignore
