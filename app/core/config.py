import os
from dataclasses import dataclass


@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "API5 Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql+pg8000")
    DB_USER: str = os.getenv("DB_USER", "analytics_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "55432")
    DB_NAME: str = os.getenv("DB_NAME", "project_analytics")

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()