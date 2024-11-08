import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Config:
    env_file = Path(__file__).parent.parent.parent / "envs" / f".env.{os.getenv('ENV', 'local')}"
    env_file_encoding = "utf-8"


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    class Config(Config):
        pass


app_settings = AppSettings()
