from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    base_api_url: str
    bot_api_token: str

    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
