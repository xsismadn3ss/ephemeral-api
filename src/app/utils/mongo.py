from pymongo import MongoClient
from pymongo.database import Database

from src.app.config import APP_Config


def get_mongo_client(config: APP_Config) -> MongoClient:
    return MongoClient(config.mongo_uri)


def get_db(config: APP_Config) -> Database:
    client = get_mongo_client(config)
    return client[config.db_name]
