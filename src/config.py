import os
from dataclasses import dataclass


@dataclass
class APP_Config:
    env: str = os.getenv("ENV", "development")
    mongo_uri: str = os.getenv("MONGO_URI", "")
