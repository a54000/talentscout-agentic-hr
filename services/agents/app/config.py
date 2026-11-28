from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Agent service settings. Values come from the environment; see .env.example."""

    model_config = SettingsConfigDict(env_prefix="AGENTS_", extra="ignore")

    env: str = "development"
    service_token: str = "dev-only-change-me"  # noqa: S105 - placeholder, overridden in every real env
    ollama_url: str = "http://localhost:11434"
    local_model: str = "qwen3:8b"
    embedding_model: str = "nomic-embed-text"


@lru_cache
def get_settings() -> Settings:
    return Settings()
