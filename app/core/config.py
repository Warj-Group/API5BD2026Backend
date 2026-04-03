import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)



@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "API5 Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql+psycopg2")
    DB_USER: str = os.getenv("DB_USER", "analytics_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "55432")
    DB_NAME: str = os.getenv("DB_NAME", "project_analytics")

    @property
    def database_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()