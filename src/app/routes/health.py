from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.utils import mongo, redis

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check(
    mongo_status: Annotated[bool, Depends(mongo.check_mongo_connection)],
    redis_status: Annotated[bool, Depends(redis.check_redis)],
):

    return {
        "status": "ok" if mongo_status and redis_status else "error",
        "db_ready": mongo_status,
        "cache_ready": redis_status,
    }
