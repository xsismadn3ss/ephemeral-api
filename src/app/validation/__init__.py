from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.config import get_config
from src.app.utils.redis import check_redis
from src.app.validation import mongo


@asynccontextmanager
async def startup(app: FastAPI):
    """
    Validaciones para MongoDB y Redis al iniciar la aplicación.
    Si alguna de las validaciones falla, se lanzará una excepción
    y la aplicación no se iniciará.
    """
    from rich.console import Console

    console = Console()

    with console.status(
        "Validando configuraciones...", spinner="bouncingBall"
    ) as status:
        status.update("Obteniendo configuraciones...")
        config = get_config()
        status.update("Validando conexión a MongoDB...")
        mongo.check_mongo(config)
        status.update("Validando índices de MongoDB...")
        mongo.check_mongo_indexes(config)
        status.update("Validando conexión a Redis...")
        check_redis(config)

    console.print("[dim]Infraestructura validada correctamente ✅[/]")
    yield
