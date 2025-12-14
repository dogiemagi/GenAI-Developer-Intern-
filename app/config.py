# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB: use Postgres in real env, SQLite for quick local
    DATABASE_URL: str = "sqlite+aiosqlite:///./linkedin.db"
    # Example Postgres URL:
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/linkedin"

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 300

    # For real scraper you may need cookies or credentials
    LINKEDIN_EMAIL: str | None = None
    LINKEDIN_PASSWORD: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
