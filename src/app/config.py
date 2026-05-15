import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def _get_optional_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None

    value = value.strip()
    return value or None


@dataclass(frozen=True)
class APP_Config:
    env = os.getenv("ENV")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "ephemeral")
    redis_host: Any = _get_optional_env("REDIS_HOST")
    redis_port: Any = _get_optional_env("REDIS_PORT")
    redis_user: Any = _get_optional_env("REDIS_USER")
    redis_password: Any = _get_optional_env("REDIS_PASSWORD")


def get_config() -> APP_Config:
    return APP_Config()


__all__ = ["get_config", "APP_Config"]
