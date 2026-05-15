from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.application.receipts_service import ReceiptAppService
from src.app.models import Receipt, ReceiptInput
from src.app.models.output import MessageOutput
from src.app.dependencies import get_receipt_app_service

router = APIRouter(prefix="/receipts", tags=["receipts"])


# listar facturas
@router.get("/", response_model=List[Receipt])
async def list_receipts(
    service: Annotated[ReceiptAppService, Depends(get_receipt_app_service)],
):
    return service.list_receipts()


# Obtener por id
@router.get("/{id}", response_model=Receipt)
async def get_receipt(
    id: str,
    service: Annotated[ReceiptAppService, Depends(get_receipt_app_service)],
):
    receipt = service.get_receipt(id)
    if receipt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
        )
    return receipt


@router.post("/", response_model=MessageOutput)
async def create_receipt(
    receipt: ReceiptInput,
    service: Annotated[ReceiptAppService, Depends(get_receipt_app_service)],
):
    result = service.create_receipt(receipt)
    return {"message": "Receipt created successfully", **result}
