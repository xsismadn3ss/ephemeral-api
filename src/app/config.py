import os
from dataclasses import dataclass


@dataclass(frozen=True)
class APP_Config:
    env: str = os.getenv("ENV", "development")
    mongo_uri: str = os.getenv("MONGO_URI", "")
    db_name: str = os.getenv("DB_NAME", "ephemeral")
