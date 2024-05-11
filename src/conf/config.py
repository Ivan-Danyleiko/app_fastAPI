from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:00000@localhost:666/fine_app"
    KEY_JWT: str = "123123"
    ALG: str = "HS256"
    MAIL_USERNAME: EmailStr = "postgres@gmail.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: str = "postgres"
    MAIL_PORT: int = 567234
    MAIL_SERVER: str = "smtp.gmail.com"
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "fine_project"
    CLD_API_KEY: int = 285493669715616
    CLD_API_SECRET: str = "secret"

    @field_validator('ALG')
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ['HS256', 'HS512']:
            raise ValueError("Invalid algorithm, must be 'HS256' or 'HS512'")
        return v

    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
