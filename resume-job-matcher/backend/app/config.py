"""
Configuration management using Pydantic Settings.
Loads environment variables and provides type-safe config access.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/resume_matcher"
    
    # File Upload
    max_file_size_mb: int = 5
    upload_dir: str = "./uploads"
    allowed_extensions: set = {".pdf"}
    
    # AI Model
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    similarity_threshold: float = 0.3  # Minimum score to consider a match
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance to avoid repeated file reads."""
    return Settings()
