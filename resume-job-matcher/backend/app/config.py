from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    app_name: str = "AI Resume-Job Matcher"
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/resume_matcher")
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-key-change-it")
    access_token_expire_minutes: int = 60 * 24  # 24 hours
    
    upload_dir: str = "uploads"
    max_file_size_mb: int = 5
    
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()