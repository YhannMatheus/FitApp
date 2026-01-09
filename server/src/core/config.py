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
    JWT_EXPIRE_DAYS: int = 1
    JWT_EXPIRE_DAYS_REMEMBER: int = 7

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def DATABASE_URL(self) -> str:
        """Retorna a URL do banco de dados baseada no ambiente (STAGE)"""
        if self.STAGE.upper() == "PROD":
            return self.PROD_DATABASE_URL
        return self.DEV_DATABASE_URL

    @property
    def DATABASE_URL_CLEAN(self) -> str:
        """Retorna a URL do banco de dados sem parâmetros incompatíveis com asyncpg"""
        url = self.DATABASE_URL
        # Remove parâmetros SSL incompatíveis com asyncpg
        if "?" in url:
            base_url = url.split("?")[0]
            return base_url
        return url


settings = Settings()  # type: ignore
