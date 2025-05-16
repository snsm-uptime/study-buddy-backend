import os
from functools import lru_cache


class Settings:
    @property
    def app_port(self) -> int:
        return int(os.getenv("APP_PORT", 8000))

    @property
    def database_url(self) -> str:
        return os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@study-buddy-db:5432/study_buddy",
        )

    @property
    def debug_port(self) -> int:
        return int(os.getenv("DEBUG_PORT", 5678))

    @property
    def env(self) -> str:
        return os.getenv("ENV", "development")

    @property
    def llm_mode(self) -> str:
        return os.getenv("LLM_MODE", "ollama")

    @property
    def ollama_base_url(self) -> str:
        return os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
