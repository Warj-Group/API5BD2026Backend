from dataclasses import dataclass


@dataclass
class Settings:
    APP_NAME: str = "API5 Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+pg8000://analytics_user:analytics123@localhost:55432/project_analytics"


settings = Settings()