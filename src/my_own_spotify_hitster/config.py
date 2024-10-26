import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configs for the MOSH application."""

    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG" if DEBUG else "WARNING"


ROOT_DIR = Path(__file__).resolve().parent.parent
settings = Settings(_env_file=ROOT_DIR.parent / ".env")  # type: ignore


logging.basicConfig()
logging.getLogger().setLevel(settings.LOG_LEVEL)

if settings.DEBUG:
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("spotipy").setLevel(logging.WARNING)
