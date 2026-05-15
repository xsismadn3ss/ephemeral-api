from typing import Annotated

from fastapi import Depends

from src.app.config import APP_Config, get_config
from src.app.services import products
from src.app.utils import mongo


def check_mongo(config: Annotated[APP_Config, Depends(get_config)]):
    health = mongo.check_mongo_connection(config)
    if not health:
        raise ConnectionError("No se pudo conectar a MongoDB")


def check_mongo_indexes(config: Annotated[APP_Config, Depends(get_config)]):
    db = mongo.get_db(config)
    indexes = products.get_indexes(db)
    # Buscar si hay indice llamadao products_expiresAt_ttl
    if "products_expiresAt_ttl" not in indexes:
        products.ensure_product_indexes(db)
        print("Product indexes ensured")
