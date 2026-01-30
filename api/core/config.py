import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    OMDB_API_KEY: str = os.getenv("OMDB_API_KEY", "")
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./movies.db")
    PROJECT_NAME: str = "Movie Note API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
