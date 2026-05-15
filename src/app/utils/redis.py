import json
from typing import Annotated

from fastapi import Depends
from redis import Redis

from src.app.config import APP_Config, get_config


def get_redis(config: Annotated[APP_Config, Depends(get_config)]):
    redis = Redis(
        host=config.redis_host,
        port=int(config.redis_port),
        username=config.redis_user,
        password=config.redis_password,
    )
    return redis


def check_redis(config: Annotated[APP_Config, Depends(get_config)]):
    # Validar configuracion
    if not isinstance(config.redis_port, str):
        port: str = config.redis_port
        if not port.isdigit():
            raise ValueError("El puerto para redis debe ser un entero")
    if not isinstance(config.redis_host, str):
        raise ValueError("El host para redis debe ser una cadena")

    # Validar cliente
    redis = get_redis(config)

    # hacer ping para validar conexion
    result = redis.ping()
    if not result:
        raise ConnectionError("No se pudo conectar a Redis")
    return True


def get_key(key: str, redis: Redis):
    cached = redis.get(key)
    if cached:
        try:
            return json.loads(cached)  # type: ignore
        except Exception:
            pass
