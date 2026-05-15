import json
from typing import Any, cast

from fastapi.encoders import jsonable_encoder
from redis import Redis


class RedisCacheRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    def get(self, key: str):
        cached = self._redis.get(key)
        if cached is None:
            return None

        if isinstance(cached, bytes):
            cached = cached.decode("utf-8")

        if not isinstance(cached, str):
            cached = cast(str, cached)

        try:
            return json.loads(cached)
        except Exception:
            return None

    def set(self, key: str, value: Any, ex: int | None = 10) -> None:
        data = json.dumps(jsonable_encoder(value))
        self._redis.set(key, data, ex=ex)

    def delete(self, key: str) -> None:
        self._redis.delete(key)
