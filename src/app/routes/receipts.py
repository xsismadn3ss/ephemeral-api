from typing import Annotated, List

from fastapi import APIRouter, Depends
from enum import Enum

from src.app.models import Receipt, ReceiptInput
from src.app.services import receipt as receipt_service
from src.app.services import cache
from src.app.utils.mongo import Database, get_db
from src.app.utils.redis import Redis, get_redis
from src.app.models.output import MessageOutput

router = APIRouter(prefix="/receipts", tags=["receipts"])


class CacheKeys(Enum):
    ALL_RECEIPTS = "receipts:all"
    RECEIPT = "receipts:{id}"


# listar facturas
@router.get("/", response_model=List[Receipt])
async def list_receipts(
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    # Intentar obtener facturas desde la caché
    receipts = cache.get(CacheKeys.ALL_RECEIPTS.value, redis)
    if receipts:
        return receipts["receipts"]

    receipts = receipt_service.list(db)

    # Guardar facturas en la caché
    cache.set(CacheKeys.ALL_RECEIPTS.value, {"receipts": receipts}, redis, ex=60 * 3)
    return receipts


# Obtener por id
@router.get("/{id}", response_model=Receipt)
async def get_receipt(
    id: str,
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):

    cache_key = CacheKeys.RECEIPT.value.format(id=id)
    receipt = cache.get(cache_key, redis)
    if receipt:
        return receipt["receipt"]

    receipt = receipt_service.get(db, id)

    # Guardar factura en la caché
    cache.set(cache_key, {"receipt": receipt}, redis, ex=60 * 3)
    return receipt


@router.post("/", response_model=MessageOutput)
async def create_receipt(
    db: Annotated[Database, Depends(get_db)],
    receipt: ReceiptInput,
    redis: Annotated[Redis, Depends(get_redis)],
):
    result = receipt_service.create(db, receipt)
    # Invalidar caché de facturas
    cache.delete(CacheKeys.ALL_RECEIPTS.value, redis)
    # Cachear nueva factura
    cache.set(
        CacheKeys.RECEIPT.value.format(id=result["receipt_id"]),
        {"receipt": result},
        redis,
        ex=60 * 3,
    )

    return {"message": "Receipt created successfully", **result}
