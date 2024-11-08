import os
from pathlib import Path

from pydantic import computed_field, MySQLDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Config:
    env_file = Path(__file__).parent.parent.parent / "envs" / f".env.{os.getenv('ENV', 'local')}"
    env_file_encoding = "utf-8"
    extra = "ignore"


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    class Config(Config):
        pass


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str

    @computed_field
    @property
    def DB_URL(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+aiomysql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_DATABASE,
        )

    class Config(Config):
        pass


app_settings = AppSettings()
database_settings = DatabaseSettings()
