import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class APP_Config:
    env = os.getenv("ENV")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "ephemeral")
    redis_host: Any = os.getenv("REDIS_HOST")
    redis_port: Any = os.getenv("REDIS_PORT")


def get_config() -> APP_Config:
    return APP_Config()
