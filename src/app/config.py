import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class APP_Config:
    env = os.getenv("ENV")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "ephemeral")


def get_config() -> APP_Config:
    return APP_Config()
