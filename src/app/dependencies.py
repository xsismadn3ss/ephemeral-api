from typing import Annotated

from fastapi import Depends
from pymongo.database import Database
from redis import Redis

from src.app.application.products_service import ProductAppService
from src.app.application.receipts_service import ReceiptAppService
from src.app.infrastructure.cache.redis_cache_repository import RedisCacheRepository
from src.app.infrastructure.mongo.products_repository import MongoProductRepository
from src.app.infrastructure.mongo.receipts_repository import MongoReceiptRepository
from src.app.utils.mongo import get_db
from src.app.utils.redis import get_redis


def get_product_app_service(
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> ProductAppService:
    return ProductAppService(
        repository=MongoProductRepository(db),
        cache=RedisCacheRepository(redis),
    )


def get_receipt_app_service(
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> ReceiptAppService:
    return ReceiptAppService(
        receipt_repository=MongoReceiptRepository(db),
        product_repository=MongoProductRepository(db),
        cache=RedisCacheRepository(redis),
    )
