from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.config import get_config
from src.app.services import products
from src.app.utils import mongo


@asynccontextmanager
async def startup(app: FastAPI):
    """
    Startup context manager for the application.
    Ensures MongoDB connection and product indexes are initialized.
    """
    config = get_config()

    health = mongo.check_mongo_connection(config)
    if not health:
        raise Exception("MongoDB connection failed")

    db = mongo.get_db(config)
    indexes = products.get_indexes(db)
    # Buscar si hay indice llamadao products_expiresAt_ttl
    if "products_expiresAt_ttl" not in indexes:
        products.ensure_product_indexes(db)
        print("Product indexes ensured")

    _indexes_initialized = True
    yield
