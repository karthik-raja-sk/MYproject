from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List
import os

class Settings(BaseSettings):
    app_name: str = "AI Resume-Job Matcher"
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/resume_matcher")
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-key-change-it")
    access_token_expire_minutes: int = 60 * 24  # 24 hours
    
    upload_dir: str = "uploads"
    max_file_size_mb: int = 5
    
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # New fields to fix validation errors from .env
    allowed_extensions: List[str] = ["pdf", "docx", "txt"]
    similarity_threshold: float = 0.3
    
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        protected_namespaces=("settings_",)
    )

@lru_cache()
def get_settings():
    return Settings()