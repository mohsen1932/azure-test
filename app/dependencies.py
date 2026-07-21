from functools import lru_cache

from app.config import Settings
from app.services.langchain_service import LangChainService


@lru_cache
def get_settings() -> Settings:
    """Provide a cached application settings instance."""
    return Settings()


@lru_cache
def get_langchain_service() -> LangChainService:
    """Provide a cached LangChain service instance for dependency injection."""
    return LangChainService()
