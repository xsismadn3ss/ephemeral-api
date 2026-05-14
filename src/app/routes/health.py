from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.utils import mongo

router = APIRouter(prefix="/health")


@router.get("")
async def health_check(
    mongo_status: Annotated[bool, Depends(mongo.check_mongo_connection)],
):

    return {
        "status": "ok" if mongo_status else "error",
        "db_connected": mongo_status,
    }
