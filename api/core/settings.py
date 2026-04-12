from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int

    URL_CORS: str
    
    ASAAS_API_KEY: str
    ASAAS_ENVIRONMENT: str
