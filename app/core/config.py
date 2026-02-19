from typing import List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Refnode"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v
    
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/Refnode")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
    
    REFERRAL_CODE_LENGTH: int = int(os.getenv("REFERRAL_CODE_LENGTH", "8"))
    REFERRAL_EXPIRY_DAYS: int = int(os.getenv("REFERRAL_EXPIRY_DAYS", "30"))
    SIGNUP_REWARD_POINTS: int = int(os.getenv("SIGNUP_REWARD_POINTS", "100"))
    REFERRER_REWARD_POINTS: int = int(os.getenv("REFERRER_REWARD_POINTS", "50"))
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()