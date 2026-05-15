import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from src.app.utils.redis import Redis, get_key


def get(key: str, redis: Redis):
    """Obtener valor de la caché por clave."""
    return get_key(key, redis)


def set(key: str, value: Any, redis: Redis, ex: int | None = 10):
    """Guardar valor en la caché con clave y opcional TTL."""
    data: ...
    if isinstance(value, dict):
        data = json.dumps(jsonable_encoder(value))
    else:
        data = value
    redis.set(key, data, ex=ex)
    print(f"[CACHE] clave: \"{key}\" actualizada")


def delete(key: str, redis: Redis):
    """Eliminar valor de la caché por clave."""
    redis.delete(key)
    print(f"[CACHE] clave: \"{key}\" eliminada")
