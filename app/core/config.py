"""Environment-aware configuration for the application."""
import os
from functools import lru_cache
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class BaseAppSettings(BaseSettings):
    """Base settings loaded from .env with sane defaults."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # App
    APP_NAME: str = "ZebOS Expert API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 3600

    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    WORKERS: int = 4

    # Agent / LLM
    AGENT_MAX_STM: int = 6
    SUMMARY_MAX_WORDS: int = 50
    OLLAMA_MODEL: str = "qwen3:4b"
    OLLAMA_CONFIG_MODEL: str = "qwen3:8b"  # used for full_configuration
    OLLAMA_TIMEOUT: int = 120

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "DEBUG"

    # Security
    ENABLE_DOCS: bool = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors_origins(cls, value):
        if isinstance(value, str):
            origins = [origin.strip() for origin in value.split(",") if origin.strip()]
            return origins or ["*"]
        return value


class DevSettings(BaseAppSettings):
    DEBUG: bool = True
    ENABLE_DOCS: bool = True
    LOG_LEVEL: str = "DEBUG"


class StagingSettings(BaseAppSettings):
    DEBUG: bool = False
    ENABLE_DOCS: bool = True
    LOG_LEVEL: str = "INFO"


class ProdSettings(BaseAppSettings):
    DEBUG: bool = False
    ENABLE_DOCS: bool = False
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = []


@lru_cache
def get_settings() -> BaseAppSettings:
    """Return settings based on ENVIRONMENT variable."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        return ProdSettings()
    if env == "staging":
        return StagingSettings()
    return DevSettings()


settings = get_settings()