from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or `.env`."""

    app_name: str = Field(default="AlgoForge", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    secret_key: str = Field(
        default="local-development-secret-change-me",
        alias="SECRET_KEY",
    )
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=14, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    database_url: str = Field(default="sqlite:///./algoforge.db", alias="DATABASE_URL")
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")
    rate_limit_requests: int = Field(default=120, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")
    ml_model_path: str = Field(default="backend/ml/artifacts/skill_estimator.joblib", alias="ML_MODEL_PATH")
    admin_email: str = Field(default="admin@algoforge.local", alias="ADMIN_EMAIL")
    admin_password: str = Field(default="change-this-password", alias="ADMIN_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )

    @property
    def model_path(self) -> Path:
        """Return the model path relative to the repository root when needed."""
        path = Path(self.ml_model_path)
        if path.is_absolute():
            return path
        return Path(__file__).resolve().parents[3] / path


@lru_cache
def get_settings() -> Settings:
    return Settings()
