"""
Application configuration
"""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    # Google Cloud settings
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "fareclock-dev")
    DATASTORE_EMULATOR_HOST: str | None = os.getenv("DATASTORE_EMULATOR_HOST", None)
    
    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8080"))
    
    # CORS settings
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        ",".join(
            [
                "http://localhost:5173",
                "http://localhost:3000",
                "http://127.0.0.1:5173",
                "https://fc-itw-esteban.web.app",
                "https://fc-itw-esteban.firebaseapp.com",
            ]
        ),
    ).split(",")
    

settings = Settings()

