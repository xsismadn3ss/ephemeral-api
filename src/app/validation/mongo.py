from typing import Annotated

from fastapi import Depends

from src.app.config import APP_Config, get_config
from src.app.infrastructure.mongo.products_repository import MongoProductRepository
from src.app.utils import mongo


def check_mongo(config: Annotated[APP_Config, Depends(get_config)]):
    client = mongo.check_mongo_connection(config)
    if not client:
        raise ConnectionError("No se pudo conectar a MongoDB")
    # Consulta sencilla para verificar que la conexión es funcional
    db = mongo.get_db(config)
    try:
        db.list_collection_names()
    except Exception as e:
        print(e)
        raise ConnectionError("La conexión a MongoDB no es funcional")


def check_mongo_indexes(config: Annotated[APP_Config, Depends(get_config)]):
    db = mongo.get_db(config)
    repository = MongoProductRepository(db)
    indexes = repository.get_indexes()
    # Buscar si hay indice llamadao products_expiresAt_ttl
    if "products_expiresAt_ttl" not in indexes:
        from rich.console import Console

        console = Console()
        repository.ensure_indexes()
        console.log("[dim]Indices de la colección 'products' asegurados[/]")
