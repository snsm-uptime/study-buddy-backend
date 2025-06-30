import os
from functools import lru_cache


class Settings:
    @property
    def app_port(self) -> int:
        return int(os.getenv("APP_PORT", 8000))

    @property
    def chroma_persist_directory(self) -> str:
        return os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    @property
    def chroma_collection_name(self) -> str:
        return os.getenv("CHROMA_COLLECTION_NAME", "ctx_collection")

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
    def max_tokens(self) -> int:
        return int(os.getenv("MAX_TOKENS", 800))

    @property
    def min_last_chunk(self) -> int:
        return int(os.getenv("MIN_LAST_CHUNK", 200))

    @property
    def ollama_host(self) -> str:
        return os.getenv("OLLAMA_HOST", "http://ollama:11434")

    @property
    def ollama_model(self) -> str:
        return os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

    @property
    def overlap_tokens(self) -> int:
        return int(os.getenv("OVERLAP_TOKENS", 50))

    @property
    def tiktoken_model(self) -> str:
        return os.getenv("TIKTOKEN_MODEL", "gpt2")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
