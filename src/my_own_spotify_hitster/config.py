from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configs for the MOSH application."""

    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000"


ROOT_DIR = Path(__file__).resolve().parent.parent
settings = Settings(_env_file=ROOT_DIR.parent / ".env")
