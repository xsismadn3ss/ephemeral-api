from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.config import get_config
from src.app.utils.redis import check_redis
from src.app.validation import mongo


@asynccontextmanager
async def startup(app: FastAPI):
    """
    Startup context manager for the application.
    Ensures MongoDB connection and product indexes are initialized.
    """
    config = get_config()
    mongo.check_mongo(config)
    mongo.check_mongo_indexes(config)
    check_redis(config)

    yield
