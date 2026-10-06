from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  

    model_config = SettingsConfigDict(
        env_prefix="NTB_",
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "NTB Toolkit"
    environment: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
