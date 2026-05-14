from typing import Annotated

from fastapi import Depends
from pymongo import MongoClient
from pymongo.database import Database

from src.app.config import APP_Config, get_config


def get_mongo_client(
    config: Annotated[APP_Config, Depends(get_config)],
) -> MongoClient:
    return MongoClient(config.mongo_uri)


def get_db(config: APP_Config) -> Database:
    client = get_mongo_client(config)
    return client[config.db_name]


def check_mongo_connection(
    config: Annotated[APP_Config, Depends(get_config)],
) -> bool:
    try:
        get_mongo_client(config)
        return True
    except Exception as e:
        print(e)
        return False
