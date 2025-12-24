"""
Configuration management for FastAPI application
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "ZebOS Expert API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    
    class ConfigDict:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
