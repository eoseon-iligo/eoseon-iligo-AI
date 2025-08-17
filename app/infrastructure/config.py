# Settings (템플릿 경로 등 환경 값)
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    templates_dir: Path = Path.cwd() / "templates"
    storage_dir: Path = Path.cwd() / "data"

    model_config = SettingsConfigDict(
        env_prefix="DOCGEN_", env_file=".env", extra="ignore"
    )


settings = Settings()
