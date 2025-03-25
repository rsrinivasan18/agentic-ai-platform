"""
Configuration settings for the Agentic AI Platform.
"""

import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional, Union
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Agentic AI Platform"
    PROJECT_DESCRIPTION: str = "A platform for building and deploying AI agents"
    PROJECT_VERSION: str = "0.1.0"

    # API settings
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"

    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Frontend
        "http://localhost:8000",  # Backend
    ]

    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "agentic_ai_platform")

    # Vector DB settings
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    # LLM settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "gpt-3.5-turbo")
    DEFAULT_EMBEDDING_MODEL: str = os.getenv(
        "DEFAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2"
    )

    # Search settings
    SERPAPI_API_KEY: Optional[str] = os.getenv("SERPAPI_API_KEY", "")

    # JWT settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 60 * 24 * 7  # 1 week in minutes

    class Config:
        case_sensitive = True


settings = Settings()
