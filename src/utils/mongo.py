from pymongo import MongoClient

from src.config import APP_Config


def get_mongo_client(config: APP_Config) -> MongoClient:
    return MongoClient(config.mongo_uri)
