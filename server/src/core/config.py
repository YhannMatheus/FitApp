from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP
    APP_NAME: str = "KiloCal"
    ENV: str = "dev"
    DEBUG: bool = False

    # STAGE
    STAGE: str = "DEV"

    # DATABASE
    DEV_DATABASE_URL: str
    PROD_DATABASE_URL: str

    # SECURITY
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def DATABASE_URL(self) -> str:
        """Retorna a URL do banco de dados baseada no ambiente (STAGE)"""
        if self.STAGE.upper() == "PROD":
            return self.PROD_DATABASE_URL
        return self.DEV_DATABASE_URL


settings = Settings()  # type: ignore
