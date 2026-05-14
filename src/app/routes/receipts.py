from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.app.models import Receipt, ReceiptInput
from src.app.services import receipt as receipt_service
from src.app.utils.mongo import Database, get_db

router = APIRouter(prefix="/receipts", tags=["receipts"])


# listar facturas
@router.get("/", response_model=List[Receipt])
async def list_receipts(
    db: Annotated[Database, Depends(get_db)],
):
    return receipt_service.list(db)


# Obtener por id
@router.get("/{id}", response_model=Receipt)
async def get_receipt(
    id: str,
    db: Annotated[Database, Depends(get_db)],
):
    return receipt_service.get(db, id)


@router.post("/")
async def create_receipt(
    db: Annotated[Database, Depends(get_db)], receipt: ReceiptInput
):
    result = receipt_service.create(db, receipt)

    return {"message": "Receipt created successfully", **result}
