
from functools import lru_cache
from pydantic_settings import BaseSettings


# See: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
class Settings(BaseSettings):
    DATABASE_DATA_PATH: str = ".dev/track_data"
    DATABASE_PATH: str = ".dev/track_data/sigmavest-track.duckdb"
    DEPENDENCY_AUTO_REGISTER: list = ["sigmavest.track.dependency"]

    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cache settings for better performance"""
    return Settings()
